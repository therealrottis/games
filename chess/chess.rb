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

def debug(position)
  temp = FEN_translator.from_FEN(position)
  Visualizer.print_board(temp)
  gets
  temp = FEN_translator.from_FEN(position)
  Visualizer.print_board(temp, true)
  gets
end

def save_position(positions) 
  prev = ""
  while true
    system("cls")
    puts
    if prev != "" then puts prev end
    puts "What do you want to save your position as? (x) to return"
    input = gets.chomp
    case input
    when "x" then return
    when "" then prev = ""
    when "s" then prev = "Invalid name"
    else
      system("cls")
      name = input
      if positions.keys.include?(name)
        x = Visualizer.make_prompt(
        "A position with this name already exists, do you want to overwrite it?")
      else x = 0 end
      unless x == 0
      else
        while true
          system("cls")
          puts
          if prev != "" then puts prev end
          puts "Input the desired position's FEN \"#{input}\" (x) to return"
          input = gets.chomp
          if input == "x" then break
          elsif input.split(" ").length != 6 then prev = "Invalid FEN/Not a FEN code" 
          else
            positions[name] = input
            positions = JSON.generate(positions)
            File.open("positions.json", "w") { |file| file.write(positions) }
            puts "Successfully added a position with name #{name}"
            puts "Enter to continue..."
            gets
            return
          end
        end
      end
    end
  end
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
      puts "---"
      positions.each do 
        |key, _| puts key
      end 
        puts "---"
        puts "(enter to continue...)"
        prev = ""
        gets
    elsif positions.include?(input) 
      debug(positions[input])
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
    puts "Exit (x)"
    input = gets.chomp.downcase
    case input
    when "x" then break 
    when "n" then debug(all_positions["start"])
    when "s" 
      save_position(all_positions)
      all_positions = JSON.parse(File.read("positions.json"))
    when "l" then load_position(all_positions)
    when "d" then debug(all_positions["test"])
    end
  end
end



main
