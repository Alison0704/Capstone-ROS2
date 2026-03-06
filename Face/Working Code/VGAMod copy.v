module VGAMod
(
    input                   CLK,
    input                   nRST,
    input                   PixelClk,

    output                  LCD_DE,
    output                  LCD_HSYNC,
    output                  LCD_VSYNC,

    output reg      [4:0]   LCD_B, // Changed to reg
    output reg      [5:0]   LCD_G, // Changed to reg
    output reg      [4:0]   LCD_R  // Changed to reg
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
reg [25:0] blink_cnt;

// Animation Timer
always @(posedge PixelClk or negedge nRST) begin
    if(!nRST) blink_cnt <= 26'd0;
    else      blink_cnt <= blink_cnt + 1'b1;
end
wire is_blinking = (blink_cnt[25:23] == 3'b111);

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

// Internal Coordinates
wire [15:0] x = (PixelCount >= H_BackPorch) ? (PixelCount - H_BackPorch) : 16'd0;
wire [15:0] y = (LineCount >= V_BackPorch) ? (LineCount - V_BackPorch) : 16'd0;

// Shape Calculations (Kept internal for logic separation)
wire eye_l, eye_r, mouth_final;

// Eyes
wire signed [31:0] dxL = $signed({16'b0, x}) - $signed(32'd250); // 400-150
wire signed [31:0] dyL = $signed({16'b0, y}) - $signed(32'd160);
assign eye_l = ((dxL*dxL + dyL*dyL) <= 32'd3600);

wire signed [31:0] dxR = $signed({16'b0, x}) - $signed(32'd550); // 400+150
wire signed [31:0] dyR = $signed({16'b0, y}) - $signed(32'd160);
assign eye_r = ((dxR*dxR + dyR*dyR) <= 32'd3600);

wire eyes_draw = (eye_l || eye_r) && (is_blinking ? (y > 155 && y < 165) : 1'b1);

// Mouth
wire m_bar = (x >= 16'd300 && x <= 16'd500 && y >= 16'd300 && y <= 16'd315);
wire signed [31:0] mx = $signed({16'b0, x}) - $signed(32'd400);
wire signed [31:0] my = $signed({16'b0, y}) - $signed(32'd315);
wire signed [31:0] m_dist = (mx*mx + my*my);
assign mouth_final = m_bar || (m_dist <= 32'd10000 && m_dist >= 32'd6400 && y >= 16'd315);

// --- REGISTERED OUTPUT LOGIC ---
// This always block ensures the colors change exactly on the clock edge, 
// removing "fuzz" and stripes.
always @(posedge PixelClk or negedge nRST) begin
    if (!nRST) begin
        LCD_R <= 5'b0;
        LCD_G <= 6'b0;
        LCD_B <= 5'b0;
    end else if (LCD_DE) begin
        if (eyes_draw || mouth_final) begin
            // Dark Blue Features
            LCD_R <= 5'h00;
            LCD_G <= 6'h00;
            LCD_B <= 5'h11;
        end else begin
            // Orange Background
            LCD_R <= 5'h1F;
            LCD_G <= 6'h29;
            LCD_B <= 5'h00;
        end
    end else begin
        // Blanking period must be black
        LCD_R <= 5'b0;
        LCD_G <= 6'b0;
        LCD_B <= 5'b0;
    end
end

endmodule