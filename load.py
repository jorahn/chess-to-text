from datasets import load_dataset
import transform

ds = load_dataset("laion/strategic_game_chess", split="train", data_files="chess_game_0001.parquet")

print(ds)

n = 0
for example in ds:
    print(example)
    print(transform.make_text_next_move(example))
    print()
    n += 1
    if n > 5:
        break