import System.Random
import Control.Monad

class (Show a) => Actor a where
    move :: String -> [a] -> a -> [a]
    rect :: a -> (Int, Int, Int, Int)  -- (x, y, w, h)

data Arena a = Arena { actors :: [a]
                     } deriving (Show)

isolate' :: [a] -> [a] -> [([a], a)]
isolate' left [] = []
isolate' left (v:right) = (left++right, v) : isolate' (v:left) right
isolate = isolate' []

tick :: (Actor a) => Arena a -> String -> Arena a
tick (Arena actors) keys = Arena $ concat $ map (uncurry $ move keys) (isolate actors)

operateArena :: (Actor a) => Arena a -> IO ()
operateArena arena = do
    print arena
    line <- getLine
    when (line /= "q") $ operateArena (tick arena line)

checkCollision :: (Actor a) => a -> a -> Bool
checkCollision a1 a2 = y2 < y1+h1 && y1 < y2+h2 && x2 < x1+w1 && x1 < x2+w2
    where
        (x1, y1, w1, h1) = rect a1
        (x2, y2, w2, h2) = rect a2

----

maxX = 320
maxY = 240
actorW = 20
actorH = 20

data BasicActor = Ball { x :: Int, y :: Int, dx :: Int, dy :: Int }
                | Ghost { x :: Int, y :: Int, rnd :: StdGen}
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
moveX (Ghost x y rnd) = Ghost x' y rnd'
    where (d, rnd') = randomR (-1,1) rnd
          x' = (x + 5 * d) `mod` maxX

moveY :: BasicActor -> BasicActor
moveY (Ball x y dx dy)
    | 0 <= y + dy && y + dy < maxY = Ball x (y + dy) dx dy
    | otherwise                    = Ball x (y - dy) dx (-dy)
moveY (Ghost x y rnd) = Ghost x y' rnd'
    where (d, rnd') = randomR (-1,1) rnd
          y' = (y + 5 * d) `mod` maxY

instance Actor BasicActor where
    rect (Ball x y _ _) = (x, y, actorW, actorH)
    rect (Ghost x y _) = (x, y, actorW, actorH)
    rect (Turtle x y _) = (x, y, actorW, actorH)
    move keys actors a@(Ball _ _ _ _) = [moveX.moveY $ foldl collide a (filter (checkCollision a) actors)]
    move keys actors (Ghost x y rnd) = if r == (0::Int) then [g, Ball x' y' 5 5] else [g]
        where (r,rnd') = randomR (0,19) rnd
              g@(Ghost x' y' _) = moveX.moveY $ Ghost x y rnd'
    move keys actors a@(Turtle _ _ _) = if (dead t) then [] else [t]
        where (Turtle x' y' dd') = foldl collide a (filter (checkCollision a) actors)
              dx = if 'a' `elem` keys then (-2) else if 'd' `elem` keys then 2 else 0
              dy = if 'w' `elem` keys then (-2) else if 's' `elem` keys then 2 else 0
              t = Turtle (max 0 (min maxX (x'+dx))) (max 0 (min maxY (y'+dy))) dd'

----

main = do
    rnd <- newStdGen
    operateArena (Arena [Ball 200 100 5 5, Ball 230 120 (-5) (-5), Ghost 100 100 rnd, Turtle 160 120 False])
    -- try to add a Wall to the actors

