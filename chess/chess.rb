require_relative "visualizer"
require_relative "fen_translator"
require_relative "piece"
require "json"

class Position  
  attr_accessor :pieces, :cmove, :castles, :en_passant, :half_moves, :move_number
  def initialize(pieces, cmove, castles, en_passant, half_moves, move_number)
    @pieces = pieces
    @cmove = cmove
    @castles = castles
    @en_passasnt = en_passant
    @half_moves = half_moves
    @move_number = move_number
  end

  def do_move(move)

  end
end

def debug
  temp = FEN_translator.from_FEN(startingpos)
  Visualizer.print_board(temp)
  gets
end

def save_position
  system("cls")
end

def load_position(positions)
  prev = ""
  while true
    system("cls")
    puts 
    if prev != "" then puts prev end
    puts "Which position do you want to load? (s) to show stored positions, (x) to return"
    input = gets.chomp.downcase
    if input == "x" then return
    elsif input == "s"
      positions.each do 
        |key, _| puts key 
        puts "(enter to continue...)"
        prev = ""
        gets
      end
    elsif positions.include?(input) 
      game(positions[input])
      return
    elsif input == ""
      prev = ""
    else 
      prev = "Position not found"
    end
  end
end

def main
  all_positions = JSON.parse(File.read("positions.json"))
  while true
    system("cls")
    puts
    puts "--- MAIN MENU ---"
    puts "New game (n)"
    puts "Save position (s)"
    puts "Load position (l)"
    puts "Debug (d)"
    puts "Misc (1)"
    puts "Exit (x)"
    input = gets.chomp.downcase
    case input
    when "x" then break 
    when "n" then game(all_positions["start"])
    when "s" 
      save_position
      all_positions = JSON.parse(File.read("positions.json"))
    when "l" then load_position(all_positions)
    when "1" then puts positions
    when "d" then debug
    end
  end
end



main
