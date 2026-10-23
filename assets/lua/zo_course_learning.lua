-- Native shared learning components for source-owned course packages.
local dir = pandoc.path.directory(debug.getinfo(1,"S").source:gsub("^@", ""))
local components = assert(loadfile(pandoc.path.join({dir,"zo_learning_components.lua"})))()
return {components.new({html = FORMAT:match("html") ~= nil})}
