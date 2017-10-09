# require 'rubygems'
# require 'open3'
# require 'json'



# stdin, stdout, stderr = Open3.popen2("python script/script.py -c script/digits_cls.pkl -i script/photo_1.jpg")
# stdout.each do |ele|
  
#   res = JSON.parse(ele) #=> [1, 2]

#   # p res
# end

# result = exec("python script/script.py -c script/digits_cls.pkl -i script/photo_1.jpg")

# puts result

require 'open3'
require 'json'

file_name = ''

ARGV.each do|a|
	file_name = "#{a}"
end

script = "python lib/assets/script.py -i " + file_name

result = ''

# stdin, stdout, stderr = Open3.popen2("python script.py -c digits_cls.pkl -i score_digit.jpg")
stdin, stdout, stderr = Open3.popen2(script)
stdout.each do |ele|
  # p ele #=> "[1, 2]\n"
  # p JSON.parse(ele) #=> [1, 2]
  res = JSON.parse(ele)
  # p res
  result += res[0].to_s + ' ' + res[1].to_s
  result += "\n"
end

puts result
