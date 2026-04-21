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
collide (Turtle x y _) (Ball _ _ _ _) = Turtle x y True
collide (Ball x y dx dy) (Ball x2 y2 _ _) = Ball x y dx dy  -- TODO
collide (Ball x y dx dy) (Turtle x2 y2 _) = Ball x y dx dy  -- TODO
collide a _ = a

instance Actor BasicActor where
    pos (Ball x y _ _) = (x, y)
    pos (Ghost x y _) = (x, y)
    pos (Turtle x y _) = (x, y)
    size a = (actorW, actorH)
    move keys colls (Ball x y dx dy) = [Ball x y dx dy] -- TODO
    move keys colls (Ghost x y rng) = [Ghost x y rng] -- TODO
    move keys actors (Turtle x y dead) = [Turtle x y dead] -- TODO

createArena rng = Arena [Ball 200 100 5 5, Ball 230 120 (-5) (-5), Ghost 100 100 rng, Turtle 160 120 False]

simulate arena = unlines.map show.take 50.scanl tick arena.takeWhile (/="x").lines

main = do
    rng <- getRng
    interact $ simulate $ createArena rng
