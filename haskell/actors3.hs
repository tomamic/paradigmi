import Xorshift

class (Show a) => Actor a where
    move :: a -> a

data Arena a = Arena { actors :: [a]
                     } deriving (Show)

tick :: (Actor a) => Arena a -> Arena a
tick (Arena actors) = Arena (map move actors)

----

maxX = 320
maxY = 240

data BasicActor = Ball { x :: Int
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
          y' = (y + 5 * d) %% maxY

instance Actor BasicActor where
    move = moveX . moveY

----

data Wall = Wall { wx :: Int
                 , wy :: Int
                 } deriving (Show)

instance Actor Wall where
    move = id    -- move w = w

----

simulate rng = unlines.map show.take 50.iterate tick $ Arena [Ball 200 100 5 5, Ghost 100 100 rng]

main = do
    rng <- getRng
    putStrLn $ simulate rng
    -- try to add a Wall to the actors

