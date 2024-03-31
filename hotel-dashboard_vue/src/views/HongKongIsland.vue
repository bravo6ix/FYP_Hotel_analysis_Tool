<template>
  <div>

    <base-header class="pb-6 pb-8 pt-5 pt-md-8 bg-gradient-success">
      <!-- Card stats -->
      <b-row>
        <b-col xl="3" md="6">
          <stats-card title="Total traffic" type="gradient-red" sub-title="350,897" icon="ni ni-active-40" class="mb-4">

            <template slot="footer">
              <span class="text-success mr-2">3.48%</span>
              <span class="text-nowrap">Since last month</span>
            </template>
          </stats-card>
        </b-col>
        <b-col xl="3" md="6">
          <stats-card title="Total traffic" type="gradient-orange" sub-title="2,356" icon="ni ni-chart-pie-35"
            class="mb-4">

            <template slot="footer">
              <span class="text-success mr-2">12.18%</span>
              <span class="text-nowrap">Since last month</span>
            </template>
          </stats-card>
        </b-col>
        <b-col xl="3" md="6">
          <stats-card title="Sales" type="gradient-green" sub-title="924" icon="ni ni-money-coins" class="mb-4">

            <template slot="footer">
              <span class="text-danger mr-2">5.72%</span>
              <span class="text-nowrap">Since last month</span>
            </template>
          </stats-card>

        </b-col>
        <b-col xl="3" md="6">
          <stats-card title="Performance" type="gradient-info" sub-title="49,65%" icon="ni ni-chart-bar-32"
            class="mb-4">

            <template slot="footer">
              <span class="text-success mr-2">54.8%</span>
              <span class="text-nowrap">Since last month</span>
            </template>
          </stats-card>
        </b-col>

        <b-col>
          <stats-card title="Total Hotel List" type="gradient-info" sub-title="49,65%" class="mb-4">
            <template>
              <span class="text-nowrap">Hotel List</span>
              <div ref="wordCloud" style="width: 600px;height:400px;"></div>
            </template>
          </stats-card>
        </b-col>

      </b-row>
    </base-header>

    <!--Charts-->
    <b-container fluid class="mt--7">
      <b-row>
        <b-col xl="8" class="mb-5 mb-xl-0">
          <card type="default" header-classes="bg-transparent">
            <b-row align-v="center" slot="header">
              <b-col>
                <h6 class="text-light text-uppercase ls-1 mb-1">Overview</h6>
                <h5 class="h3 text-white mb-0">Sales value</h5>
              </b-col>
              <b-col>
                <b-nav class="nav-pills justify-content-end">
                  <b-nav-item class="mr-2 mr-md-0" :active="bigLineChart.activeIndex === 0" link-classes="py-2 px-3"
                    @click.prevent="initBigChart(0)">
                    <span class="d-none d-md-block">Month</span>
                    <span class="d-md-none">M</span>
                  </b-nav-item>
                  <b-nav-item link-classes="py-2 px-3" :active="bigLineChart.activeIndex === 1"
                    @click.prevent="initBigChart(1)">
                    <span class="d-none d-md-block">Week</span>
                    <span class="d-md-none">W</span>
                  </b-nav-item>
                </b-nav>
              </b-col>
            </b-row>
            <line-chart :height="350" ref="bigChart" :chart-data="bigLineChart.chartData"
              :extra-options="bigLineChart.extraOptions">
            </line-chart>
          </card>
        </b-col>

        <b-col xl="4" class="mb-5 mb-xl-0">
          <card header-classes="bg-transparent">
            <b-row align-v="center" slot="header">
              <b-col>
                <h6 class="text-uppercase text-muted ls-1 mb-1">Performance</h6>
                <h5 class="h3 mb-0">Total orders</h5>
              </b-col>
            </b-row>

            <bar-chart :height="350" ref="barChart" :chart-data="redBarChart.chartData">
            </bar-chart>
          </card>
        </b-col>
      </b-row>
      <!-- End charts-->

      <!--Tables-->
      <b-row class="mt-5">
        <b-col xl="8" class="mb-5 mb-xl-0">
          <page-visits-table></page-visits-table>
        </b-col>
        <b-col xl="4" class="mb-5 mb-xl-0">
          <social-traffic-table></social-traffic-table>
        </b-col>
      </b-row>
      <!--End tables-->
    </b-container>

  </div>
</template>
<script>
import axios from 'axios';

// Charts
import * as chartConfigs from '@/components/Charts/config';
import LineChart from '@/components/Charts/LineChart';
import BarChart from '@/components/Charts/BarChart';
import * as echarts from 'echarts';
import 'echarts-wordcloud';

// Components
import BaseProgress from '@/components/BaseProgress';
import StatsCard from '@/components/Cards/StatsCard';

// Tables
import SocialTrafficTable from './Dashboard/SocialTrafficTable';
import PageVisitsTable from './Dashboard/PageVisitsTable';

export default {
  components: {
    LineChart,
    BarChart,
    BaseProgress,
    StatsCard,
    PageVisitsTable,
    SocialTrafficTable
  },
  data() {
    return {
      wordCloudChart: null,
      wordCloudData: [],
      bigLineChart: {
        allData: [],
        chartData: null,
        activeIndex: 0,
        extraOptions: null,
      },
      redBarChart: {
        chartData: {
          labels: ['Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
          datasets: [{
            label: 'Sales',
            data: [25, 20, 30, 22, 17, 29]
          }]
        },
        wordCloudChart: null,
        extraOptions: chartConfigs.blueChartOptions
      }
    };
  },

  methods: {
    initBigChart() {
      const labels = ['May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
      let chartData = {
        datasets: [{
          label: 'Performance',
          data: labels.map(label => {
            const item = this.bigLineChart.allData.find(data => data.month === label);
            return item ? item.totalAmount : 0;
          })
        }],
        labels: labels,
      };
      this.bigLineChart.chartData = chartData;
    },

  },

  async created() {
    try {
      const response = await axios.get('http://localhost:3001/api/services/month-sum-price');
      const response2 = await axios.get('http://localhost:3001/api/services/hotels/hongkongisland');

      // response 1
      this.bigLineChart.allData = response.data;
      this.initBigChart();

      // response 2
      this.wordCloudData = response2.data;
      this.wordCloudChart = echarts.init(this.$refs.wordCloud);
      this.wordCloudChart.setOption({
        series: [{
          type: 'wordCloud',
          data: this.wordCloudData,
          textStyle: {
            normal: {
              fontSize: function (data) {
                // set the font size based on the value
                return data.value;
              }
            }
          },
          rotationRange: [0,0],
        }]
      });

    } catch (error) {
      console.error('Error fetching data:', error);
    };
  },

  mounted() {
    if (!this.bigLineChart.allData.length) {
      this.initBigChart();
    };

    // Resize the wordcloud chart
    this.wordCloudChart.resize();
  },
};
</script>
<style>
.el-table .cell {
  padding-left: 0px;
  padding-right: 0px;
}
</style>