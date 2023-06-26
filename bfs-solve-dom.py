from pyscript import Element, display
import js

import asyncio

# Configure!
animDelay = 20  # in ms
startColor = "pink"
endColor = "yellow"
puzzleColor = "lime"
pathColor = "darkgreen"

# The py-splashscreen doesn't seem to autoclose when explicitly added to the DOM.
# But it is useful to explicitly add py-splashscreen to the DOM to prevent layout jitters.
js.document.querySelector("py-splashscreen").style.display = "none"

biggrid = Element('biggrid')
# print("BIGGRID:", biggrid.select("div"))

rows = js.document.querySelectorAll(".row")
sideSize = len(rows)
# sideSize = 20

# start = biggrid.select("div[data-x='0'][data-y='0']")
start = js.document.querySelector("div[data-x='0'][data-y='0']")
start.style.backgroundColor = startColor

# end = biggrid.select(f"div[data-x='{sideSize - 1}'][data-y='{sideSize - 1}']")
end = js.document.querySelector(f"div[data-x='{sideSize - 1}'][data-y='{sideSize - 1}']")
end.style.backgroundColor = endColor

allDirs = [[0, -1], [1, 0], [0, 1], [-1, 0]]  # N, E, S, W in [dx, dy]
visit = [start]

# while(len(visit) > 0):  # PyScript doesn't refresh screen after each DOM update. So, we need to async it.
finished = False  # Short circuit return for async loop calls that process after end is found.
count = 0  # Get an idea of how many times the loop is run, looking for the end.
async def loop():
    global finished, count

    if finished: return

    count += 1
    display("LOOP: " + str(count), target="pythonOutput", append=False)

    curr = visit.pop(0)
    # print("CURR:", curr.dataset.x, curr.dataset.y, curr)

    if curr == end:
        display("FINISHED! " + str(count) + " LOOPS.", target="pythonOutput", append=False)
        finished = True
        for e in js.document.querySelectorAll(".col"):
            if e != end and e != start:
                e.style.backgroundColor = puzzleColor

        while hasattr(curr.dataset, 'prevX') and curr != start:
            if curr != end and curr != start:
                curr.style.backgroundColor = pathColor
            curr = js.document.querySelector(f"div[data-x='{curr.dataset.prevX}'][data-y='{curr.dataset.prevY}']")
            # print("PREV:", curr.dataset.x, curr.dataset.y)
        # break
        return

    if curr != start:
        curr.style.backgroundColor = pathColor

    # Get neighbors and go to wherever is open.
    currX = int(curr.dataset.x)
    currY = int(curr.dataset.y)
    for dir in allDirs:
        newX = currX + dir[0]
        newY = currY + dir[1]

        # First check if new coords are within the maze area.
        if newX >= 0 and newX < sideSize and newY >= 0 and newY < sideSize:
            # Then check to see if it's a valid direction
            # print("WALLS: N: ", curr.style.borderTop, " E: ", curr.style.borderRight, " S: ", curr.style.borderBottom, " W: ", curr.style.borderLeft)
            if dir[1] != 0:
                if dir[1] == -1:
                    if curr.style.borderTop != "none": continue
                else:
                    if curr.style.borderBottom != "none": continue
            else:
                if dir[0] == -1:
                    if curr.style.borderLeft != "none": continue
                else:
                    if curr.style.borderRight != "none": continue

            # const neighbor = biggrid.children[newY].children[newX];
            neighbor = js.document.querySelector(f"div[data-x='{newX}'][data-y='{newY}']")
            # print("NEIGH:", newX, newY, neighbor)
            if not neighbor.style.backgroundColor == pathColor and not neighbor in visit:
                neighbor.dataset.prevX = currX
                neighbor.dataset.prevY = currY
                visit.append(neighbor)

    # time.sleep(animDelay / 1000)
    await asyncio.sleep(animDelay / 1000)
    await loop()

display("STARTING...", target="pythonOutput", append=False)
asyncio.ensure_future(loop())