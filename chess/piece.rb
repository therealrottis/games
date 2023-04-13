class Piece
  attr_accessor :color, :piece, :symbol, :piece_text

  def pieces
    {"1k" => "♔",
    "1q" => "♕",
    "1r" => "♖",
    "1b" => "♗",
    "1n" => "♘",
    "1p" => "♙",
    "0k" => "♚",
    "0q" => "♛",
    "0r" => "♜",
    "0b" => "♝",
    "0n" => "♞",
    "0p" => "♟︎",
    "-1" => " "}
  end

  def pieces_text
    {"k" => "King",
    "q" => "Queen",
    "r" => "Rook",
    "b" => "Bishop",
    "n" => "Knight",
    "p" => "Pawn",
    "" => ""}
  end

  def initialize(color, piece)
    @color = color # white = 1, black = 0, empty = -1
    @piece = piece # k, q, r, b, n, p, ""
    @symbol = pieces[color.to_s + piece]
    ptype = "Empty"
    if color == 1 then ptype = "White "
    elsif color == 0 then ptype = "Black "
    end
    @piece_text = ptype + pieces_text[piece]
  end

  def to_s
    @symbol
  end

  def calculate_moves(board, x, y)
    if @piece == "" then return end
    
  end
end
