require_relative "piece"
class FEN_translator
  def self.from_FEN(fen)
    fen = fen.split(" ")
    cur = fen[0].split("/")
    nboard = []
    cur.each do |rank|
      crank = []
      rank.each_char do |piece| 
        if ("1".."8").include?(piece)
          piece.to_i.times { crank << Piece.new(-1, "") }
        else
          crank << Piece.new((piece == piece.upcase) ? 1 : 0, piece.downcase)
        end
      end
      nboard << crank
    end
    return nboard
  end

  def self.to_FEN
    false
  end
end