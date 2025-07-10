<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <link rel="stylesheet" href="/CSS/index.css">
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.6/dist/css/bootstrap.min.css" rel="stylesheet">
  <script rel="stylesheet" src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.6/dist/js/bootstrap.bundle.min.js"></script>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.5/font/bootstrap-icons.css" rel="stylesheet">
  <title>Admin Dashboard</title>
  <style>
    body{
      display: flex;
      min-height: 100vh;
    }
    /* Main content */
    .main {
      margin-left: 25% ;
      flex: 1;
      padding: 20px;
    }

    .header {
      background-color: #fff;
      padding: 10px 20px;
      margin-bottom: 20px;
      box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }

    .cards {
      display: flex;
      gap: 20px;
      flex-wrap: wrap;
    }

    .card {
      background-color: white;
      padding: 20px;
      border-radius: 8px;
      flex: 1;
      min-width: 200px;
      box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }

    .card h3 {
      margin-bottom: 10px;
    }
  </style>
</head>
<body>
  <header id="header-admin"></header>

  <div class="main">
    <div class="header">
      <h1>Bienvenido al panel de administración</h1>
    </div>

    <div class="cards">
      <div class="card">
        <h3>Usuarios</h3>
        <p>135 registrados</p>
        
      </div>
      <div class="card">
        <h3>Ventas</h3>
        <p>34 este mes</p>
      </div>
      <div class="card">
        <h3>Ingresos</h3>
        <p>$4,500</p>
      </div>
    </div>
  </div>
</body>
</html>

<script>
  fetch('header-admin.html').then(res=>res.text())
  .then(data =>{document.getElementById("header-admin").innerHTML = data})


  // <block:setup:2>
const DATA_COUNT = 12;
Utils.srand(110);

const actions = [
  {
    name: 'Randomize',
    handler(chart) {
      chart.data.datasets.forEach(dataset => {
        dataset.data = generateData();
      });
      chart.update();
    }
  },
];
// </block:setup>

// <block:data:1>
function generateData() {
  return Utils.numbers({
    count: DATA_COUNT,
    min: 0,
    max: 100
  });
}

const data = {
  labels: Utils.months({count: DATA_COUNT}),
  datasets: [{
    data: generateData()
  }]
};
// </block:data>

// <block:options:0>
function getLineColor(ctx) {
  return Utils.color(ctx.datasetIndex);
}

function alternatePointStyles(ctx) {
  const index = ctx.dataIndex;
  return index % 2 === 0 ? 'circle' : 'rect';
}

function makeHalfAsOpaque(ctx) {
  return Utils.transparentize(getLineColor(ctx));
}

function adjustRadiusBasedOnData(ctx) {
  const v = ctx.parsed.y;
  return v < 10 ? 5
    : v < 25 ? 7
    : v < 50 ? 9
    : v < 75 ? 11
    : 15;
}

const config = {
  type: 'line',
  data: data,
  options: {
    plugins: {
      legend: false,
      tooltip: true,
    },
    elements: {
      line: {
        fill: false,
        backgroundColor: getLineColor,
        borderColor: getLineColor,
      },
      point: {
        backgroundColor: getLineColor,
        hoverBackgroundColor: makeHalfAsOpaque,
        radius: adjustRadiusBasedOnData,
        pointStyle: alternatePointStyles,
        hoverRadius: 15,
      }
    }
  }
};
// </block:options>

module.exports = {
  actions,
  config,
};
</script>
</html>