class Visualizer 
  def self.array_to_str(array)
    output = ""
    array.each do |row|
      row.each do |cell|
        output += cell.to_s + " |"
      end
      output += "\n"
    end
    output
  end

  def self.print_board(board, flip = false)
    files = (1..8).reverse_each
    board.each do |row|
      row.unshift(files.next)
    end
    header = [" ", "a", "b", "c", "d", "e", "f", "g", "h"]
    if flip
      board.push(header)
    else
      board.unshift(header)
    end
    unless flip
      board.each do |row| 
        row.reverse!
        row.unshift(row[-1])
        row.pop[-1]
      end 
      board.reverse!
    end
    Visualizer.print_array(board)
  end

  def self.print_array(array)
    system "cls"
    puts
    puts Visualizer.array_to_str(array)
  end

  def self.make_prompt(text, option1 = "Yes", option2 = "No", option1prompt = "y", option2prompt = "n")
    system "cls"
    puts
    puts "#{text} (#{option1prompt}/#{option2prompt})"
    puts
    puts "#{option1} | #{option2}"
    input = gets.chomp.downcase
    return (input == option1prompt) ? 0 : ((input == option2prompt) ? 1 : -1)
  end
end
