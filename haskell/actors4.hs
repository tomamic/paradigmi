import System.Random
import Control.Monad

class (Show a) => Actor a where
    move :: String -> [a] -> a -> [a]
    rect :: a -> (Int, Int, Int, Int)  -- (x, y, w, h)

data Arena a = Arena { actors :: [a]
                     } deriving (Show)

tick :: (Actor a) => Arena a -> String -> Arena a
tick (Arena actors) keys = Arena $ concat (map (move keys actors) actors)

operateArena :: (Actor a) => Arena a -> IO ()
operateArena arena = do
    print arena
    line <- getLine
    when (line /= "q") $ operateArena (tick arena line)

checkCollision :: (Actor a) => a -> a -> Bool
checkCollision a1 a2 = (rect a1) /= (rect a2) && y2 < y1+h1 && y1 < y2+h2 && x2 < x1+w1 && x1 < x2+w2
    where
        (x1, y1, w1, h1) = rect a1
        (x2, y2, w2, h2) = rect a2

maxX = 320
maxY = 240
actorW = 20
actorH = 20

data BasicActor = Ball { x :: Int, y :: Int, dx :: Int, dy :: Int }
                | Ghost { x :: Int, y :: Int, rnd :: StdGen}
                | Turtle { x :: Int, y :: Int, dead :: Bool} deriving (Show)

collide :: BasicActor -> BasicActor -> BasicActor
collide (Ball x y _ _) (Ball x2 y2 _ _) = Ball … -- TODO
collide (Ball x y _ _) (Turtle x2 y2 _) = Ball … -- TODO
collide (Turtle x y _) (Ball _ _ _ _) = Turtle … -- TODO
collide a _ = a

instance Actor BasicActor where
    rect (Ball x y _ _) = (x, y, actorW, actorH)
    rect (Ghost x y _) = (x, y, actorW, actorH)
    rect (Turtle x y _) = (x, y, actorW, actorH)
    move keys actors (Ball x y dx dy) = … -- TODO
    move keys actors (Ghost x y rnd) = … -- TODO
    move keys actors (Turtle x y dead) = … -- TODO

main = do
    rnd <- newStdGen
    operateArena (Arena [Ball 200 100 5 5, Ball 230 120 (-5) (-5), Ghost 100 100 rnd, Turtle 160 120 False])

