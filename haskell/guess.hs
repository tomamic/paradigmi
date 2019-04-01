import System.Random

process gen ("":ls) = []
process gen ls =
    "Which number (1-10) am I thinking of?":
        answer:
        process newGen (tail ls)
        -- if correct then [] else (process newGen (tail ls))
    where
        (secret, newGen) = randomR (1,10) gen :: (Int, StdGen)
        correct = read (head ls) == secret
        answer = if correct
            then "You are correct!"
            else "Sorry, it was " ++ show secret

main = do
    gen <- getStdGen
    interact $ unlines . (process gen) . lines
