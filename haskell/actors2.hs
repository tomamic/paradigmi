import Xorshift

maxX = 320
maxY = 240

data BasicActor = Ball    { x :: Int
                          , y :: Int
                          , dx :: Int
                          , dy :: Int
                  }
                  | Ghost { x :: Int
                          , y :: Int
                          , rng :: Rng
                  } deriving (Show)

moveX :: BasicActor -> BasicActor
moveX (Ball x y dx dy)
    | 0 <= x + dx && x + dx < maxX = Ball (x + dx) y dx dy
    | otherwise                    = Ball (x - dx) y (-dx) dy
moveX (Ghost x y rng) = Ghost x' y rng'
    where (d, rng') = randint (-1,1) rng
          x' = (x + 5 * d) %% maxX

moveY :: BasicActor -> BasicActor
moveY (Ball x y dx dy)
    | 0 <= y + dy && y + dy < maxY = Ball x (y + dy) dx dy
    | otherwise                    = Ball x (y - dy) dx (-dy)
moveY (Ghost x y rng) = Ghost x y' rng'
    where (d, rng') = randint (-1,1) rng
          y' = (y + 5 * d) `mod` maxY

move :: BasicActor -> BasicActor
move = moveX . moveY

data BasicArena = BasicArena { actors :: [BasicActor]
                             } deriving (Show)

tick :: BasicArena -> BasicArena
tick (BasicArena actors) = BasicArena (map move actors)

simulate rng = unlines.map show.take 50.iterate tick $ BasicArena [Ball 200 100 5 5, Ghost 100 100 rng]

main = do
    rng <- getRng
    putStrLn $ simulate rng
