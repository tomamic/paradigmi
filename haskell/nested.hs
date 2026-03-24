data Nested a = NVal a
              | NLst [Nested a]
              deriving (Show, Read, Eq)

sumNested (NVal v) = v
sumNested (NLst l) = sum $ map sumNested l

vals = NLst [NLst [NVal 1, NVal 2, NLst [NVal 3, NVal 4], NLst [NVal 5]], NVal 6]

main = print $ sumNested vals
