import Xorshift

class (Show a) => Actor a where
    move :: String -> [a] -> a -> [a]
    pos :: a -> (Int, Int)  -- (x, y)
    size :: a -> (Int, Int) -- (w, h)

data Arena a = Arena { actors :: [a]
                     } deriving (Show)

tick :: (Actor a) => Arena a -> String -> Arena a
tick (Arena actors) keys = Arena $ concat $ map (uncurry $ move keys) (allCollisions actors)

allCollisions actors = map (actorCollisions iactors) iactors
    where iactors = zip [0..] actors

actorCollisions iactors (i,a) = (map snd (filter (checkCollision (i,a)) iactors), a)

checkCollision :: (Actor a) => (Int,a) -> (Int,a) -> Bool
checkCollision (i1,a1) (i2,a2) = i1 /= i2 && y2 < y1+h1 && y1 < y2+h2 && x2 < x1+w1 && x1 < x2+w2
    where
        (x1, y1) = pos a1
        (x2, y2) = pos a2
        (w1, h1) = size a1
        (w2, h2) = size a2

----

maxX = 320
maxY = 240
actorW = 20
actorH = 20

data BasicActor = Ball { x :: Int, y :: Int, dx :: Int, dy :: Int }
                | Ghost { x :: Int, y :: Int, rng :: Rng}
                | Turtle { x :: Int, y :: Int, dead :: Bool} deriving (Show)

collide :: BasicActor -> BasicActor -> BasicActor
collide (Ball x1 y1 _ _) (Ball x2 y2 _ _) = Ball x1 y1 (if x1 < x2 then -5 else 5) (if y1 < y2 then -5 else 5)
collide (Ball x1 y1 _ _) (Turtle x2 y2 _) = Ball x1 y1 (if x1 < x2 then -5 else 5) (if y1 < y2 then -5 else 5)
collide (Turtle x1 y1 _) (Ball x2 y2 dx2 dy2) = Turtle x1 y1 True
collide a _ = a

moveX :: BasicActor -> BasicActor
moveX (Ball x y dx dy)
    | 0 <= x + dx && x + dx < maxX = Ball (x + dx) y dx dy
    | otherwise                    = Ball (x - dx) y (-dx) dy
moveX (Ghost x y rng) = Ghost x' y rng'
    where (d, rng') = randint (-1,1) rng
          x' = (x + 5 * d) `mod` maxX

moveY :: BasicActor -> BasicActor
moveY (Ball x y dx dy)
    | 0 <= y + dy && y + dy < maxY = Ball x (y + dy) dx dy
    | otherwise                    = Ball x (y - dy) dx (-dy)
moveY (Ghost x y rng) = Ghost x y' rng'
    where (d, rng') = randint (-1,1) rng
          y' = (y + 5 * d) `mod` maxY

instance Actor BasicActor where
    pos (Ball x y _ _) = (x, y)
    pos (Ghost x y _) = (x, y)
    pos (Turtle x y _) = (x, y)
    size a = (actorW, actorH)
    move keys colls a@(Ball _ _ _ _) = [moveX.moveY $ foldl collide a colls]
    move keys colls (Ghost x y rng) = if r == (0::Int) then [g, Ball x' y' 5 5] else [g]
        where (r,rng') = randint (0,19) rng
              g@(Ghost x' y' _) = moveX.moveY $ Ghost x y rng'
    move keys colls a@(Turtle _ _ _) = if (dead t) then [] else [t]
        where (Turtle x' y' dd') = foldl collide a colls
              dx = if 'a' `elem` keys then (-2) else if 'd' `elem` keys then 2 else 0
              dy = if 'w' `elem` keys then (-2) else if 's' `elem` keys then 2 else 0
              t = Turtle (max 0 (min maxX (x'+dx))) (max 0 (min maxY (y'+dy))) dd'

----

createArena rng = Arena [Ball 200 100 5 5, Ball 230 120 (-5) (-5), Ghost 100 100 rng, Turtle 160 120 False]

simulate arena = unlines.map show.take 50.scanl tick arena.takeWhile (/="x").lines

main = do
    rng <- getRng
    interact $ simulate $ createArena rng
