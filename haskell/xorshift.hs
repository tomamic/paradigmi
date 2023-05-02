import Data.Word (Word32)
import Data.Bits (xor, shiftL, shiftR)
import Data.Time.Clock.POSIX (getPOSIXTime)

type Rng32 = Word32

xorshift32 :: Rng32 -> Rng32
xorshift32 a = d where
  b = a `xor` (a `shiftL` 13)
  c = b `xor` (b `shiftR` 17)
  d = c `xor` (c `shiftL` 5)

randint :: (Int, Int) -> Rng32 -> (Int, Rng32)
randint (nmin, nmax) gen = (val, nxt) where
    nxt = xorshift32 gen
    val = nmin + (fromIntegral nxt) `mod` (nmax + 1 - nmin)

randints :: (Int, Int) -> Rng32 -> [Int]
randints range gen =
    val : randints range nxt
    where (val, nxt) = randint range gen

chunksOf n [] = []
chunksOf n xs = a : chunksOf n b where
  (a, b) = splitAt n xs

getRng32 :: IO Rng32
getRng32 = do
    now <- getPOSIXTime
    return (round (now * 1000) :: Rng32)
