require 'io/console'
require 'colorize'

class Board
  def initialize
  @board = [[0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 2, 0, 0],
            [0, 0, 0, 0]]
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
      if row[0] == row[1] || row[1] == row[2] || row[2] == row[3]
        debug_log("ch2", :hasmoves)
        return true
      end
    }
    (0..3).each { |index|
      if @board[0][index] == @board[1][index] ||
         @board[1][index] == @board[2][index] ||
         @board[2][index] == @board[3][index] 
        debug_log("ch3", :hasmoves)
        return true    
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
      while row.length < 4
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
    @board.each { |row| 
      puts "+------"*4 + "+"
      puts "|      "*4 + "|"
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
        print "| #{c} "
        }
      puts "|"
      puts "|      "*4 + "|"
    }
    puts "+------"*4 + "+"
  end

  def board
    @board
  end
end

def add_color(text)
  case text
  when " 2  "
    text.light_black
  when " 4  "
    text.light_white
  when " 8  "
    text.yellow
  when " 16 "
    text.green
  when " 32 "
    text.light_green
  when " 64 "
    text.blue
  when "128 "
    text.light_blue
  when "256 "
    text.cyan
  when "512 "
    text.magenta
  when "1024"
    text.light_magenta
  when "2048"
    text.red
  else
    text
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
    puts input
  end
end

def main
  board = Board.new
  $core = 0
  while board.has_moves?
    char = STDIN.getch
    if char == "x" || char == "\u0003"
      puts "..."
      exit(1)
    end
    debug_log(char, :input)
    move = -1
    case char
      when "\x00K" #left
        move = 0
      when "\x00M" #right
        move = 1
      when "\x00H" #up
        move = 2
      when "\x00P" #down
        move = 3
    end
    unless move == -1
      move = board.do_move(move)
      unless move = false
        system("cls")
        puts
        puts "Score: #{$core}"
        puts
        board.display
        puts
      end
    end
  end
  puts "gg"
end
 
main
