module Nested where

data Nested a = NVal a
              | NLst [Nested a]
              deriving (Show, Read, Eq)

nestedSum (NVal v) = v
nestedSum (NLst l) = sum $ map nestedSum l

-- main = print $ nestedSum vals where
--     vals = NLst [NLst [NVal 1, NVal 2, NLst [NVal 3, NVal 4], NLst [NVal 5]], NVal 6]
