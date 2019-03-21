merge :: (Ord a) => [a] -> [a] -> [a]
merge [] xs = xs
merge xs [] = xs
merge (x:xs) (y:ys)
    | x <= y = x : merge xs (y:ys)
    | otherwise = y : merge (x:xs) ys

mergeSort :: (Ord a) => [a] -> [a]
mergeSort [] = []
mergeSort [x] = [x]
mergeSort xs = merge (mergeSort (take n xs)) (mergeSort (drop n xs))
    where n = length xs `div` 2

-- mergeSort xs = merge (mergeSort as) (mergeSort bs)
--    where (as, bs) = splitAt (length xs `div` 2) xs
