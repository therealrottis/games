require 'io/console'
begin
  require 'colorize'
rescue LoadError => e
  p e
  puts
  puts "Download the 'colorize' gem to add colors"
  puts
end

class Board
  def initialize(mode)
    case mode
    when :debug
      $BSIZE = 4
      @board = [[2, 4, 8, 16],
                [32, 64, 128, 256],
                [512, 1024, 2048, 0],
                [9, 10, 11, 12]]
      return
    end
    @board = []
    row = []
    $BSIZE.times { row.push(0) }
    $BSIZE.times { @board.push(row) } 
    self.new_random
  end

  def has_empty?
    @board.each { |row| 
      row.each { |cell| 
        if cell == 0
          return true
        end
      }
    }
    false
  end

  def has_moves?
    if self.has_empty?
      debug_log("ch1", :hasmoves)
      return true
    end
    @board.each { |row|
      (1..$BSIZE).each do |i|
        if row[i-1] == row[i]
          debug_log("ch2", :hasmoves)
          return true
        end
      end
    }
    (0..$BSIZE-1).each { |index|
      (1..$BSIZE-1).each do |x|
        if @board[x-1][index] == @board[x][index] 
          debug_log("ch3", :hasmoves)
          return true    
        end
      end
    }
    false
  end

  def new_random
    empties = 0
    emptiesdict = {}
    @board.each_with_index { |row, y| 
      row.each_with_index { |cell, x| 
        if cell == 0
          emptiesdict[empties] = [y, x]
          empties += 1
        end
      }
    }
    loc = emptiesdict[Random.rand(empties)]
    if rand(4) == 0
      value = 4
    else
      value = 2
    end
    @board[loc[0]][loc[1]] = value
    debug_log(emptiesdict.to_s, :random)
  end

  def do_move(move)
    og_board = Marshal.load(Marshal.dump(@board))
    if move >= 2
      @board = matrix_transpose(@board)
      transpose = true
      move -= 2
    else
      transpose = false
    end
    if move == 1
      @board.each { |row| row.reverse! }
      flip = true
    else
      flip = false
    end
    @board.each_with_index do |r, i|
      row = r.select {|x| x != 0}
      nrow = []
      while row.length > 0
        if row[0] == row[1]
          nrow.push(row[0]*2)
          $core += row[0]*2
          row.shift(2)
        else
          nrow.push(row[0])
          row.shift
        end
      end
      if row.length == 1
        nrow.push(row[0])
      end
      row = nrow
      while row.length < $BSIZE
        row.push(0)
      end
      @board[i] = row
    end
    if flip
      @board.each { |row| row.reverse! }
    end
    if transpose
      @board = matrix_transpose(@board)
    end
    if og_board == @board
      return false
    end
    if self.has_empty?
      self.new_random
    end
  end

  def display
    output = ""
    @board.each { |row| 
      output += "+------"*$BSIZE + "+\n"
      output += "|      "*$BSIZE + "|\n"
      row.each { |cell| 
        c = cell.to_s
        unless cell == 0
          if c.to_s.length <= 2
            c = " #{c.to_s} "
          end
          if c.to_s.length == 3
            c = "#{c.to_s} "
          end
        else
          c = "    "
        end
        c = add_color(c)
        output += "| #{c} "
        }
      output += "|\n"
      output += "|      "*$BSIZE + "|\n"
    }
    output += "+------"*$BSIZE + "+\n"
    output
  end

  def board
    @board
  end
end

def add_color(text)
  begin
    case text
    when " 2  "
      text.black
    when " 4  "
      text
    when " 8  "
      text.yellow
    when " 16 "
      text.light_yellow
    when " 32 "
      text.light_green
    when " 64 "
      text.blue
    when "128 "
      text.light_cyan
    when "256 "
      text.magenta
    when "512 "
      text.light_magenta
    when "1024"
      text.red
    when "2048"
      text.light_red
    when " 9  " # debug colors
      text.light_cyan
    when " 10 "
      text.light_green
    when " 11 "
      text.green
    when " 12 "
      text.light_yellow
    else
      text
    end
  rescue NoMethodError => e
    return text
  end
end

#black
#light_black  
#red
#light_red    
#green        
#light_green  
#yellow       
#light_yellow 
#blue
#light_blue   
#magenta      
#light_magenta
#cyan
#light_cyan   
#white        
#light_white  
#default   

def matrix_transpose(matrix)
  output = []
  matrix[0].length.times { output.push([]) }
  matrix.each { |row|
    row.each_with_index {|cell, i|
      output[i].push(cell)
    }
  }
  output
end

def debug_log(input, type)
  #:hasmoves, :input, :random
  enabled_types = []
  if enabled_types.include? type
    p input
  end
end

def main
  $core = 0
  $BSIZE = 5
  board = Board.new(:n)
  puts "WASD to begin..."
  while board.has_moves?
    if true
      char = STDIN.getch
    else
      char = "wasd"[rand(4)]
    end
    if char == "x" || char == "\u0003"
      puts "..."
      exit(1)
    end
    debug_log(char, :input)
    move = -1
    char.downcase!
    case char
      when "\x00k" then move = 0 #left
      when "\xE0k" then move = 0
      when "a" then move = 0
      when "\x00m" then move = 1 #right
      when "\xE0m" then move = 1
      when "d" then move = 1
      when "\x00h" then move = 2 #up
      when "\xE0h" then move = 2
      when "w" then move = 2
      when "\x00p" then move = 3 #down
      when "\xE0p" then move = 3
      when "s" then move = 3
    end
    unless move == -1
      move = board.do_move(move)
      unless move == false
        d = board.display
        system("cls") || system('clear')
        puts
        puts "Score: #{$core}"
        puts
        puts d
        puts
      end
    end
  end
  puts "Game over!"
end

main
