-- Marsaglia https://doi.org/10.18637/jss.v008.i14

import Data.Word (Word64)
import Data.Bits (xor, shiftL, shiftR)
import Data.Time.Clock.POSIX (getPOSIXTime)
import GHC.Exts (sortWith)

type Rng = Word64
(%%) = mod

xorshift :: Rng -> Rng
xorshift a = d where
  b = a `xor` (a `shiftL` 13)
  c = b `xor` (b `shiftR` 7)
  d = c `xor` (c `shiftL` 17)

constrain :: (Int, Int) -> Rng -> Int
constrain (nmin, nmax) n = fromIntegral n %% (nmax+1-nmin) + nmin

randint :: (Int, Int) -> Rng -> (Int, Rng)
randint range gen = (constrain range gen, xorshift gen)

randints :: (Int, Int) -> Rng -> [Int]
randints range gen = map (constrain range) $ iterate xorshift gen

shuffle :: [a] -> Rng -> ([a], Rng)
shuffle vals gen = (shuffled, nxt) where
    (rs, nxt:_) = splitAt (length vals) $ iterate xorshift gen
    shuffled = map snd $ sortWith fst $ zip rs vals

chunksOf n [] = []
chunksOf n xs = a : chunksOf n b where
  (a, b) = splitAt n xs

getRng :: IO Rng
getRng = do
    now <- getPOSIXTime
    return (round (now * 1000) :: Rng)
