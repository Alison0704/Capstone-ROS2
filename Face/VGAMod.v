module VGAMod
(
    input                   CLK,
    input                   nRST,
    input                   PixelClk,

    output                  LCD_DE,
    output                  LCD_HSYNC,
    output                  LCD_VSYNC,

    output reg      [4:0]   LCD_B, 
    output reg      [5:0]   LCD_G, 
    output reg      [4:0]   LCD_R  
);

// Timing Parameters
localparam [15:0] V_BackPorch = 16'd6;
localparam [15:0] V_Pluse     = 16'd5; 
localparam [15:0] HightPixel  = 16'd480;
localparam [15:0] V_FrontPorch= 16'd62; 
localparam [15:0] H_BackPorch = 16'd182;  
localparam [15:0] H_Pluse     = 16'd1; 
localparam [15:0] WidthPixel  = 16'd800;
localparam [15:0] H_FrontPorch= 16'd210;

localparam [15:0] PixelForHS  = WidthPixel + H_BackPorch + H_FrontPorch;     
localparam [15:0] LineForVS   = HightPixel + V_BackPorch + V_FrontPorch;

reg [15:0] LineCount, PixelCount;
reg [26:0] anim_cnt;

// Animation Timer
always @(posedge PixelClk or negedge nRST) begin
    if(!nRST) anim_cnt <= 27'd0;
    else      anim_cnt <= anim_cnt + 1'b1;
end

wire is_blinking = (anim_cnt[26:24] == 3'b111);
wire mouth_open  = anim_cnt[23]; // Slow movement

// Sync Logic
always @(posedge PixelClk or negedge nRST) begin
    if(!nRST) begin LineCount <= 16'd0; PixelCount <= 16'd0; end
    else if(PixelCount == PixelForHS) begin
        PixelCount <= 16'd0;
        LineCount <= (LineCount == LineForVS) ? 16'd0 : LineCount + 1'b1;
    end else PixelCount <= PixelCount + 1'b1;
end

assign LCD_HSYNC = (PixelCount < H_Pluse) ? 1'b0 : 1'b1;
assign LCD_VSYNC = (LineCount < V_Pluse) ? 1'b0 : 1'b1;
assign LCD_DE    = (PixelCount >= H_BackPorch && PixelCount < (H_BackPorch + WidthPixel) && 
                    LineCount >= V_BackPorch  && LineCount < (V_BackPorch + HightPixel));

wire [15:0] x = (PixelCount >= H_BackPorch) ? (PixelCount - H_BackPorch) : 16'd0;
wire [15:0] y = (LineCount >= V_BackPorch) ? (LineCount - V_BackPorch) : 16'd0;

// --- EYES ---
wire signed [31:0] dxL = $signed({16'b0, x}) - $signed(32'd250);
wire signed [31:0] dyL = $signed({16'b0, y}) - $signed(32'd160);
wire eye_l = ((dxL*dxL + dyL*dyL) <= 32'd3600);

wire signed [31:0] dxR = $signed({16'b0, x}) - $signed(32'd550);
wire signed [31:0] dyR = $signed({16'b0, y}) - $signed(32'd160);
wire eye_r = ((dxR*dxR + dyR*dyR) <= 32'd3600);

wire eyes_draw = (eye_l || eye_r) && (is_blinking ? (y > 155 && y < 165) : 1'b1);

// --- MOUTH LOGIC ---
// The bar (flat part) is always visible
wire m_bar = (x >= 16'd300 && x <= 16'd500 && y >= 16'd300 && y <= 16'd310);

// The hollow curve only renders when mouth_open is true
wire signed [31:0] mx = $signed({16'b0, x}) - $signed(32'd400);
wire signed [31:0] my = $signed({16'b0, y}) - $signed(32'd310);
wire [31:0] m_dist = (mx*mx + my*my);
wire m_curve = (mouth_open && m_dist <= 32'd10000 && m_dist >= 32'd8100 && y >= 16'd310);

wire mouth_draw = m_bar || m_curve;

// --- COLOR OUTPUT ---
always @(posedge PixelClk or negedge nRST) begin
    if (!nRST) begin
        LCD_R <= 5'h0; LCD_G <= 6'h0; LCD_B <= 5'h0;
    end else if (LCD_DE) begin
        if (eyes_draw || mouth_draw) begin
            LCD_R <= 5'h1F;
            LCD_G <= 6'h29;
            LCD_B <= 5'h00;
        end else begin
            LCD_R <= 5'h00;
            LCD_G <= 6'h00;
            LCD_B <= 5'h11;
        end
    end else begin
        LCD_R <= 5'h0; LCD_G <= 6'h0; LCD_B <= 5'h0;
    end
end

endmodule