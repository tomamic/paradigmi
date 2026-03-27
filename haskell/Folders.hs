module Folders where

data Elem = Document String String
          | Folder String [Elem]
          deriving (Show, Read, Eq)

elemSize (Document _ content) = length content
elemSize (Folder _ nodes) = sum $ map elemSize nodes

-- main = print $ elemSize desktopF where
--     prodD = Document "prod.csv" "1,2,3,4"
--     dataF = Folder "data" [prodD]
--     a1_0D = Document "a1.txt" "bla bla 0"
--     workF = Folder "Work" [a1_0D, dataF]
--     a1_1D = Document "a1.txt" "a different file"
--     personalF = Folder "Personal" [a1_1D]
--     desktopF = Folder "Desktop" [workF, personalF]
