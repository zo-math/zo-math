function Table(t)
  local n = #t.colspecs
  local widths = ({[3]={0.14,0.44,0.42},[4]={0.10,0.30,0.30,0.30},[6]={0.17,0.13,0.13,0.22,0.09,0.26}})[n]
  if widths then
    for i=1,n do t.colspecs[i] = {t.colspecs[i][1], widths[i]} end
  end
  return t
end
