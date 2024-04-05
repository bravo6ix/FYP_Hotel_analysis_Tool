<template>

  <b-card body-class="p-0" header-class="border-0">
    <template v-slot:header>
      <b-row align-v="center">
        <b-col>
          <h3 class="mb-0">Hotel List</h3>
        </b-col>
        <!-- <b-col class="text-right">
          <a href="#!" class="btn btn-sm btn-primary">See all</a>
        </b-col> -->
      </b-row>
    </template>

    <el-table class="table-responsive table"
              :data="tableData"
              header-row-class-name="thead-light">
      <el-table-column label="Hotel Name"
                       min-width="130px"
                       prop="hotel">
        <template v-slot="{row}">
          <div class="font-weight-600">{{row.hotel}}</div>
        </template>
      </el-table-column>
      <el-table-column label="Count"
                       min-width="70px"
                       prop="count">
      </el-table-column>
      <el-table-column label="District"
                       min-width="120px"
                       prop="district">
      </el-table-column>

      <el-table-column label="Rating"
                       min-width="90px"
                       prop="rating">
        <template v-slot="{row}">
          {{row.rating}}
        </template>
      </el-table-column>
    </el-table>
  </b-card>
</template>
<script>
  import { Table, TableColumn, DropdownMenu, DropdownItem, Dropdown} from 'element-ui'
  import axios from 'axios';
  export default {
    name: 'hotel-visits-table',
    components: {
      [Table.name]: Table,
      [TableColumn.name]: TableColumn,
      [Dropdown.name]: Dropdown,
      [DropdownItem.name]: DropdownItem,
      [DropdownMenu.name]: DropdownMenu,
    },
    data() {
      return {
        tableData: [
          {
            hotel: 'Ibis Hong Kong Central & Sheung Wan',
            count: '4',
            district: 'Hong Kong Island',
            rating: '8.2'
          },
          {
            hotel: 'BEST WESTERN PLUS Hotel Hong Kong',
            count: '3',
            district: 'Hong Kong Island',
            rating: '6.8'
          },
          {
            hotel: 'Ramada Hong Kong Harbour View',
            count: '3',
            district: '294',
            rating: '6.3'
          },
          {
            hotel: 'Hyatt Centric Victoria Harbour',
            count: '2',
            district: 'Hong Kong Island',
            rating: '7.9'
          },
          {
            hotel: 'The Royal Garden',
            count: '4',
            district: 'Yau Tsim Mong',
            rating: '7.8'
          }
        ]
      }


    }

  }
</script>
<style>
</style>
