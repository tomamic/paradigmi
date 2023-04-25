import System.Random

process :: [Int] -> [String] -> [String]
process secrets guesses =
    "Which number (1-10) am I thinking of?" : check secrets guesses

check :: [Int] -> [String] -> [String]
check _ ("":_) = []
check (secret:secrets) (guess:guesses)
    | guess == show secret = ["You are correct!"]
    | otherwise = ("Sorry, it was " ++ show secret) : process secrets guesses

main = do
    gen <- getStdGen
    let secrets = randomRs (1,10) gen
    interact $ unlines . (process secrets) . lines
