<template>
  <div id="columns">
    <div class="column">
      <Plotly class="graph" :data="data1" :layout="layout1" :display-mode-bar="false"></Plotly>
      <Plotly class="graph" :data="data2" :layout="layout2" :display-mode-bar="false"></Plotly>
      <Plotly class="graph" :data="data3" :layout="layout3" :display-mode-bar="false"></Plotly>
    </div>
    <div class="column">
      <Plotly class="graph" :data="data4" :layout="layout4" :display-mode-bar="false"></Plotly>
      <Plotly class="graph" :data="data5" :layout="layout5" :display-mode-bar="false"></Plotly>
      <Plotly class="graph" :data="data6" :layout="layout6" :display-mode-bar="false"></Plotly>
    </div>
  </div>
</template>

<script>
import { Plotly } from "vue-plotly";

export default {
  name: "Graphs",
  components: {
    Plotly
  },
  props: {
    start: Number,
    stop: Number,
    data1: Array,
    data2: Array,
    data3: Array,
    data4: Array,
    data5: Array,
    data6: Array
  },
  data() {
    return {
      // ----- LAYOUT 1 -----
      layout1: {
        title: "<b>Direct Sequences</b>",
        titlefont: {
          family: "Avenir, Helvetica, Arial, sans-serif",
          size: 16
        },
        autosize: false,
        width: 590,
        height: 200,
        margin: {
          l: 52,
          r: 50,
          b: 30,
          t: 30,
          pad: 4
        },
        spikedistance: 200,
        hoverdistance: 100,
        xaxis: {
          showgrid: false,
          showline: true,
          linewidth: 2,
          ticks: "outside",
          ticklen: 7,
          tickwidth: 2,
          tickfont: {
            family: "Avenir, Helvetica, Arial, sans-serif",
            size: 12,
            color: "black"
          },
          dtick: 200,
          showcrossline: true,
          spikemode: "across",
          spikecolor: "green",
          spikedash: "solid",
          spikethickness: 2
        },
        yaxis: {
          title: "Frame 1",
          titlefont: {
            family: "Avenir, Helvetica, Arial, sans-serif",
            size: 14,
            color: "grey"
          },
          showgrid: false,
          showline: true,
          linewidth: 2,
          ticks: "outside",
          ticklen: 7,
          tickwidth: 2,
          tickfont: {
            family: "Avenir, Helvetica, Arial, sans-serif",
            size: 12,
            color: "black"
          },
          range: [0, 1],
          dtick: 0.5,
          tickformat: ".1f"
        },
        shapes: [
          {
            type: "line",
            x0: this.start,
            y0: 0,
            x1: this.start,
            yref: "paper",
            y1: 1,
            line: {
              color: "red",
              width: 1.5,
              dash: "dot"
            }
          },
          {
            type: "line",
            x0: this.stop,
            y0: 0,
            x1: this.stop,
            yref: "paper",
            y1: 1,
            line: {
              color: "red",
              width: 1.5,
              dash: "dot"
            }
          }
        ],
        annotations: [
          {
            x: this.start,
            y: 1,
            xref: "x",
            yref: "y",
            text: "current<br>start",
            font: {
              family: "Avenir, Helvetica, Arial, sans-serif",
              size: 11,
              color: "black"
            },
            showarrow: true,
            ax: 0,
            ay: -20
          },
          {
            x: this.stop,
            y: 1,
            xref: "x",
            yref: "y",
            text: "current<br>stop",
            font: {
              family: "Avenir, Helvetica, Arial, sans-serif",
              size: 11,
              color: "black"
            },
            showarrow: true,
            ax: 0,
            ay: -20
          }
        ]
      },
      // ----- LAYOUT 2 -----
      layout2: {
        autosize: false,
        width: 590,
        height: 200,
        margin: {
          l: 52,
          r: 50,
          b: 30,
          t: 30,
          pad: 4
        },
        spikedistance: 200,
        hoverdistance: 100,
        xaxis: {
          showgrid: false,
          showline: true,
          linewidth: 2,
          ticks: "outside",
          ticklen: 7,
          tickwidth: 2,
          tickfont: {
            family: "Avenir, Helvetica, Arial, sans-serif",
            size: 12,
            color: "black"
          },
          dtick: 200,
          showcrossline: true,
          spikemode: "across",
          spikecolor: "green",
          spikedash: "solid",
          spikethickness: 2
        },
        yaxis: {
          title: "Frame 2",
          titlefont: {
            family: "Avenir, Helvetica, Arial, sans-serif",
            size: 14,
            color: "grey"
          },
          showgrid: false,
          showline: true,
          linewidth: 2,
          ticks: "outside",
          ticklen: 7,
          tickwidth: 2,
          tickfont: {
            family: "Avenir, Helvetica, Arial, sans-serif",
            size: 12,
            color: "black"
          },
          range: [0, 1],
          dtick: 0.5,
          tickformat: ".1f"
        },
        shapes: [
          {
            type: "line",
            x0: this.start,
            y0: 0,
            x1: this.start,
            yref: "paper",
            y1: 1,
            line: {
              color: "red",
              width: 1.5,
              dash: "dot"
            }
          },
          {
            type: "line",
            x0: this.stop,
            y0: 0,
            x1: this.stop,
            yref: "paper",
            y1: 1,
            line: {
              color: "red",
              width: 1.5,
              dash: "dot"
            }
          }
        ]
      },
      // ----- LAYOUT 3 -----
      layout3: {
        autosize: false,
        width: 590,
        height: 225,
        margin: {
          l: 52,
          r: 50,
          b: 60,
          t: 30,
          pad: 4
        },
        spikedistance: 200,
        hoverdistance: 100,
        xaxis: {
          title: "Nucleotide Position",
          titlefont: {
            family: "Avenir, Helvetica, Arial, sans-serif",
            size: 14,
            color: "grey"
          },
          showgrid: false,
          showline: true,
          linewidth: 2,
          ticks: "outside",
          tickfont: {
            family: "Avenir, Helvetica, Arial, sans-serif",
            size: 12,
            color: "black"
          },
          ticklen: 7,
          tickwidth: 2,
          dtick: 200,
          showcrossline: true,
          spikemode: "across",
          spikecolor: "green",
          spikedash: "solid",
          spikethickness: 2
        },
        yaxis: {
          title: "Frame 3",
          titlefont: {
            family: "Avenir, Helvetica, Arial, sans-serif",
            size: 14,
            color: "grey"
          },
          showgrid: false,
          showline: true,
          linewidth: 2,
          ticks: "outside",
          tickfont: {
            family: "Avenir, Helvetica, Arial, sans-serif",
            size: 12,
            color: "black"
          },
          ticklen: 7,
          tickwidth: 2,
          range: [0, 1],
          dtick: 0.5,
          tickformat: ".1f"
        },
        shapes: [
          {
            type: "line",
            x0: this.start,
            y0: 0,
            x1: this.start,
            yref: "paper",
            y1: 1,
            line: {
              color: "red",
              width: 1.5,
              dash: "dot"
            }
          },
          {
            type: "line",
            x0: this.stop,
            y0: 0,
            x1: this.stop,
            yref: "paper",
            y1: 1,
            line: {
              color: "red",
              width: 1.5,
              dash: "dot"
            }
          }
        ]
      },
      // ----- LAYOUT 4 -----
      layout4: {
        title: "<b>Complementary Sequences</b>",
        titlefont: {
          family: "Avenir, Helvetica, Arial, sans-serif",
          size: 16
        },
        autosize: false,
        width: 590,
        height: 200,
        margin: {
          l: 52,
          r: 50,
          b: 30,
          t: 30,
          pad: 4
        },
        spikedistance: 200,
        hoverdistance: 100,
        xaxis: {
          showgrid: false,
          showline: true,
          linewidth: 2,
          ticks: "outside",
          ticklen: 7,
          tickwidth: 2,
          dtick: 200,
          tickfont: {
            family: "Avenir, Helvetica, Arial, sans-serif",
            size: 12,
            color: "black"
          },
          showcrossline: true,
          spikemode: "across",
          spikecolor: "green",
          spikedash: "solid",
          spikethickness: 2
        },
        yaxis: {
          title: "Frame 4",
          titlefont: {
            family: "Avenir, Helvetica, Arial, sans-serif",
            size: 14,
            color: "grey"
          },
          showgrid: false,
          showline: true,
          linewidth: 2,
          ticks: "outside",
          ticklen: 7,
          tickwidth: 2,
          range: [0, 1],
          dtick: 0.5,
          tickformat: ".1f",
          tickfont: {
            family: "Avenir, Helvetica, Arial, sans-serif",
            size: 12,
            color: "black"
          }
        },
        shapes: [
          {
            type: "line",
            x0: this.start,
            y0: 0,
            x1: this.start,
            yref: "paper",
            y1: 1,
            line: {
              color: "red",
              width: 1.5,
              dash: "dot"
            }
          },
          {
            type: "line",
            x0: this.stop,
            y0: 0,
            x1: this.stop,
            yref: "paper",
            y1: 1,
            line: {
              color: "red",
              width: 1.5,
              dash: "dot"
            }
          }
        ],
        annotations: [
          {
            x: this.start,
            y: 1,
            xref: "x",
            yref: "y",
            text: "current<br>start",
            font: {
              family: "Avenir, Helvetica, Arial, sans-serif",
              size: 11,
              color: "black"
            },
            showarrow: true,
            ax: 0,
            ay: -20
          },
          {
            x: this.stop,
            y: 1,
            xref: "x",
            yref: "y",
            text: "current<br>stop",
            font: {
              family: "Avenir, Helvetica, Arial, sans-serif",
              size: 11,
              color: "black"
            },
            showarrow: true,
            ax: 0,
            ay: -20
          }
        ]
      },
      // ----- LAYOUT 5 -----
      layout5: {
        autosize: false,
        width: 590,
        height: 200,
        margin: {
          l: 52,
          r: 50,
          b: 30,
          t: 30,
          pad: 4
        },
        spikedistance: 200,
        hoverdistance: 100,
        xaxis: {
          showgrid: false,
          showline: true,
          linewidth: 2,
          ticks: "outside",
          ticklen: 7,
          tickwidth: 2,
          dtick: 200,
          tickfont: {
            family: "Avenir, Helvetica, Arial, sans-serif",
            size: 12,
            color: "black"
          },
          showcrossline: true,
          spikemode: "across",
          spikecolor: "green",
          spikedash: "solid",
          spikethickness: 2
        },
        yaxis: {
          title: "Frame 5",
          titlefont: {
            family: "Avenir, Helvetica, Arial, sans-serif",
            size: 14,
            color: "grey"
          },
          showgrid: false,
          showline: true,
          linewidth: 2,
          ticks: "outside",
          ticklen: 7,
          tickwidth: 2,
          range: [0, 1],
          dtick: 0.5,
          tickformat: ".1f",
          tickfont: {
            family: "Avenir, Helvetica, Arial, sans-serif",
            size: 12,
            color: "black"
          }
        },
        shapes: [
          {
            type: "line",
            x0: this.start,
            y0: 0,
            x1: this.start,
            yref: "paper",
            y1: 1,
            line: {
              color: "red",
              width: 1.5,
              dash: "dot"
            }
          },
          {
            type: "line",
            x0: this.stop,
            y0: 0,
            x1: this.stop,
            yref: "paper",
            y1: 1,
            line: {
              color: "red",
              width: 1.5,
              dash: "dot"
            }
          }
        ]
      },
      // ----- LAYOUT 6 -----
      layout6: {
        autosize: false,
        width: 590,
        height: 225,
        margin: {
          l: 52,
          r: 50,
          b: 60,
          t: 30,
          pad: 4
        },
        spikedistance: 200,
        hoverdistance: 100,
        xaxis: {
          title: "Nucleotide Position",
          titlefont: {
            family: "Avenir, Helvetica, Arial, sans-serif",
            size: 14,
            color: "grey"
          },
          showgrid: false,
          showline: true,
          linewidth: 2,
          ticks: "outside",
          ticklen: 7,
          tickwidth: 2,
          dtick: 200,
          tickfont: {
            family: "Avenir, Helvetica, Arial, sans-serif",
            size: 12,
            color: "black"
          },
          showcrossline: true,
          spikemode: "across",
          spikecolor: "green",
          spikedash: "solid",
          spikethickness: 2
        },
        yaxis: {
          title: "Frame 6",
          titlefont: {
            family: "Avenir, Helvetica, Arial, sans-serif",
            size: 14,
            color: "grey"
          },
          showgrid: false,
          showline: true,
          linewidth: 2,
          ticks: "outside",
          ticklen: 7,
          tickwidth: 2,
          range: [0, 1],
          dtick: 0.5,
          tickformat: ".1f",
          tickfont: {
            family: "Avenir, Helvetica, Arial, sans-serif",
            size: 12,
            color: "black"
          }
        },
        shapes: [
          {
            type: "line",
            x0: this.start,
            y0: 0,
            x1: this.start,
            yref: "paper",
            y1: 1,
            line: {
              color: "red",
              width: 1.5,
              dash: "dot"
            }
          },
          {
            type: "line",
            x0: this.stop,
            y0: 0,
            x1: this.stop,
            yref: "paper",
            y1: 1,
            line: {
              color: "red",
              width: 1.5,
              dash: "dot"
            }
          }
        ]
      }
    };
  }
};
</script>

<style scoped>
.columns:after {
  display: table;
  clear: both;
}

.column {
  width: 50%;
  float: left;
}

/* --------------------- */
/* Responsive Design */
@media only screen and (max-width: 1200px) {
  .column {
    width: 100%;
    margin-bottom: 30px;
  }
}
</style>