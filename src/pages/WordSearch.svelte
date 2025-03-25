<script>
  const gridSize = 10;
  const answerWord = "APPLE";

  let grid = [];
  let isDragging = false;
  let startRow = null;
  let startCol = null;
  let direction = null;
  let hasEnded = false;
  let showModal = false;

  let highlighted = Array.from({ length: gridSize }, () =>
    Array.from({ length: gridSize }, () => false)
  );

  const directions = [
    { dx: 1, dy: 0 },
    { dx: -1, dy: 0 },
    { dx: 1, dy: 1 },
    { dx: -1, dy: -1 },
  ];

  function generateGrid() {
    grid = Array.from({ length: gridSize }, () =>
      Array.from({ length: gridSize }, () => "")
    );

    const dir = directions[Math.floor(Math.random() * directions.length)];
    const reversed = Math.random() < 0.5;
    const word = reversed ? [...answerWord].reverse().join("") : answerWord;

    let placed = false;
    while (!placed) {
      const row = Math.floor(Math.random() * gridSize);
      const col = Math.floor(Math.random() * gridSize);

      let fits = true;
      for (let i = 0; i < word.length; i++) {
        const r = row + dir.dy * i;
        const c = col + dir.dx * i;
        if (r < 0 || r >= gridSize || c < 0 || c >= gridSize) {
          fits = false;
          break;
        }
      }

      if (fits) {
        for (let i = 0; i < word.length; i++) {
          const r = row + dir.dy * i;
          const c = col + dir.dx * i;
          grid[r][c] = word[i];
        }
        placed = true;
      }
    }

    for (let r = 0; r < gridSize; r++) {
      for (let c = 0; c < gridSize; c++) {
        if (!grid[r][c]) {
          grid[r][c] = String.fromCharCode(65 + Math.floor(Math.random() * 26));
        }
      }
    }

    highlighted = Array.from({ length: gridSize }, () =>
      Array.from({ length: gridSize }, () => false)
    );
  }

  generateGrid();

  function startDrag(row, col) {
    isDragging = true;
    startRow = row;
    startCol = col;
    direction = null;
    highlighted = Array.from({ length: gridSize }, () =>
      Array.from({ length: gridSize }, () => false)
    );
    highlighted[row][col] = true;
    highlighted = [...highlighted];
  }

  function highlightCell(row, col) {
    if (!isDragging || highlighted[row][col]) return;

    const count = highlighted.flat().filter(Boolean).length;
    if (count >= 5) return;

    if (!direction) {
      const dx = col - startCol;
      const dy = row - startRow;

      if (
        (dx === 0 && dy !== 0) ||
        (dy === 0 && dx !== 0) ||
        (Math.abs(dx) === Math.abs(dy) && dx !== 0)
      ) {
        direction = {
          dx: dx / Math.abs(dx || dy),
          dy: dy / Math.abs(dx || dy),
        };
      } else {
        return;
      }
    }

    const expectedRow = startRow + direction.dy * count;
    const expectedCol = startCol + direction.dx * count;

    if (row === expectedRow && col === expectedCol) {
      highlighted[row][col] = true;
      highlighted = [...highlighted];
    }
  }

  function endDrag() {
    if (hasEnded) return;
    hasEnded = true;

    isDragging = false;

    const selected = [];
    for (let r = 0; r < gridSize; r++) {
      for (let c = 0; c < gridSize; c++) {
        if (highlighted[r][c]) {
          selected.push({ row: r, col: c });
        }
      }
    }

    const sorted = selected.sort((a, b) => {
      const aIndex =
        direction.dy * (a.row - startRow) + direction.dx * (a.col - startCol);
      const bIndex =
        direction.dy * (b.row - startRow) + direction.dx * (b.col - startCol);
      return aIndex - bIndex;
    });

    const word = sorted.map(({ row, col }) => grid[row][col]).join("");

    if (word === answerWord) {
      console.log("✅ 정답입니다!");
      showModal = true; // ✅ 모달 표시
    } else {
      console.log(`❌ 정답이 아닙니다. 현재 선택된 값은 ${word} 입니다.`);
    }

    startRow = null;
    startCol = null;
    direction = null;
    highlighted = Array.from({ length: gridSize }, () =>
      Array.from({ length: gridSize }, () => false)
    );

    setTimeout(() => {
      hasEnded = false;
    }, 200);
  }

  function resetGame() {
    showModal = false;
    generateGrid();
  }

  window.addEventListener("mouseup", endDrag);
</script>

<main on:mouseup={endDrag}>
  <h1>단어 찾기 게임: APPLE</h1>

  <div class="grid">
    {#each grid as row, rowIndex}
      {#each row as letter, colIndex}
        <div
          class="cell"
          on:mousedown={() => startDrag(rowIndex, colIndex)}
          on:mouseenter={() => highlightCell(rowIndex, colIndex)}
          style="background-color: {highlighted[rowIndex][colIndex]
            ? 'blue'
            : 'white'};"
        >
          {letter}
        </div>
      {/each}
    {/each}
  </div>

  {#if showModal}
    <div class="modal-backdrop">
      <div class="modal">
        <p>🎉 정답입니다!</p>
        <button on:click={resetGame}>확인</button>
      </div>
    </div>
  {/if}
</main>

<style>
  main {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 20px;
    user-select: none;
  }

  .grid {
    display: grid;
    grid-template-columns: repeat(10, 40px);
    grid-template-rows: repeat(10, 40px);
    gap: 4px;
    margin-top: 20px;
  }

  .cell {
    width: 40px;
    height: 40px;
    border: 1px solid black;
    box-sizing: border-box;
    cursor: pointer;
    transition: background-color 0.1s;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: bold;
    font-size: 18px;
  }

  .modal-backdrop {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.4);
    display: flex;
    justify-content: center;
    align-items: center;
  }

  .modal {
    background: white;
    padding: 30px;
    border-radius: 10px;
    text-align: center;
    font-size: 20px;
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
  }

  .modal button {
    margin-top: 15px;
    padding: 10px 20px;
    font-size: 16px;
    cursor: pointer;
  }
</style>
