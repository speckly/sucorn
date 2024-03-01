import os
import time

TOKEN = "1BVN0AcXfFQA_fSi_vTdeu_LJSPcj0p_WP4eOo_b5SpOnbEJEPdyL0LTc0Po07xNuc8sHUTcZHZmQBnL8IxCfVYdyuXHqRAAH4IdmNby_8dr8f1UH7Si6fSYEphpcZArrqkCmHWQgg57FOvZsQoGBZILoN74xhF69HSMxWqP0vC_yqXORmWPhGv6L9K8RP-DrV3_eZP6Yb0RcsSN-PeMWPMfkWp7ZuXci9-XEN0MdPr4"
PROMPT = "an anime girl with cat ears energetan anime girl with cat ears energetically jumping and leaping and bouncing on a big space hopper ball with a handle, both ball and handle must be of the same color, ball is plain, girl is sitting on the ball and is holding onto its handle, girl's feet must be in front of the ball and pointing towards the floor, ball off the ground and very high up in the air, space hopper ball has a big handle, field of flowers, colored, closeup perspective from below the ball"
OUT_PATH = "..\..\sucorn_bot\images\catgirls-24"
a = f"py BingImageCreator.py -U {TOKEN} --prompt \"{PROMPT}\" --output-dir {OUT_PATH}"

count = 0
while True:
    s = time.time()
    count += 1
    os.system(a)
    print(f"{count}: {time.time()-s}s")

    