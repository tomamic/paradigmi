rev_tr :: [a] -> [a] -> [a]
rev_tr [] acc = acc
rev_tr (x:xs) acc = rev_tr xs (x:acc)

reverse' xs = rev_tr xs []
