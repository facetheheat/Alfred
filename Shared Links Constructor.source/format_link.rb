#!/usr/bin/ruby

url = ARGV[0]

case url
  when /^(smb:\/\/)/
    a1 = url.clone.gsub(/^(([^:\/??#]+?):)??(\/\/)/imx, "\\\\\\")
    a2 = a1.gsub!("\/", "\\")
    puts a2
    b1 = url.clone.gsub("smb", "afp")
    puts b1
    c1 = url.clone.gsub("smb", "cifs")
    puts c1
    puts url

  when /^(cifs:)/
    a2 = url.clone.gsub(/^(([^:\/??#]+?):)??(\/\/)/imx, "\\\\\\")
    a3 = a2.gsub!("\/", "\\")
    puts a3
    b1 = url.clone.gsub("cifs", "afp")
    puts b1
    c1 = url.clone.gsub("cifs", "cifs")
    puts c1
    puts url
    
  when /^(\/\/)/
    a1 = url.clone.gsub(/^(([^:\/??#]+?):)??(\/\/)/imx, "\\\\\\")
    a2 = a1.gsub!("\/", "\\")
    puts a2
    b1 = url.clone.gsub("//", "afp://")
    puts b1
    c1 = url.clone.gsub("//", "smb://")
    puts c1
    d1 = url.clone.gsub("//", "cifs://")
    puts d1    
    puts url
    
  when /^(\\)/
    a1 = url.clone.gsub(/^(([\\+\\]))/imx, "//")
    a2 = a1.gsub!("\\", "/")
    a3 = a2.gsub!("///", "//")
    puts a3
    
    b1 = a3.clone.gsub("//", "afp://")
    puts b1
    c1 = a3.clone.gsub("//", "smb://")
    puts c1
    d1 = a3.clone.gsub("//", "cifs://")
    puts d1    
    puts url
  
  when /^(afp:)/
    a2 = url.clone.gsub(/^(([^:\/??#]+?):)??(\/\/)/imx, "\\\\\\")
    a3 = a2.gsub!("\/", "\\")
    puts a3
    b1 = url.clone.gsub("afp", "smb")
    puts b1
    c1 = url.clone.gsub("afp", "cifs")
    puts c1
    puts url
  else
    print "Unknown URL\n"
    exit 1
end
