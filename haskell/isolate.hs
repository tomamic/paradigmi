isolate' :: [a] -> [a] -> [([a], a)]
isolate' left [] = []
isolate' left (v:right) = (left++right, v) : isolate' (v:left) right
isolate = isolate' []

main = print $ isolate "aeiou"
