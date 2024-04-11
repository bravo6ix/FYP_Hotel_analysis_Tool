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

    <el-table class="table-responsive table" :data="sortedData" @sort-change="handleSort"
      header-row-class-name="thead-light">

      <el-table-column label="Hotel Name" min-width="130px" prop="hotel" sortable="custom">
        <template v-slot="{ row }">
          <div class="font-weight-600">{{ row.hotel }}</div>
        </template>
      </el-table-column>

      <el-table-column label="Count" min-width="150px" prop="count" sortable="custom">

      </el-table-column>
      <el-table-column label="District" min-width="120px" prop="district" sortable="custom">
      </el-table-column>

      <el-table-column label="Rating" min-width="100px" prop="rating" sortable="custom">
        <template v-slot="{ row }">
          {{ row.rating }}
        </template>
      </el-table-column>

      <el-table-column label="Reviews" min-width="100px" prop="views" sortable="custom">
        <template v-slot="{ row }">
          {{ row.views }}
        </template>
      </el-table-column>
    </el-table>
  </b-card>
</template>
<script>
import { Table, TableColumn, DropdownMenu, DropdownItem, Dropdown } from 'element-ui'
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
      tableData: [],
      sort: {
        prop: '',
        order: '',
      },
    }
  },
  async created() {
    try {
      const response = await axios.get('http://localhost:3001/api/services/hotels/district/Yautsimmong');
      this.tableData = response.data.map(item => ({
        hotel: item.hotel_name,
        count: item.count.toString(),
        district: item.district,
        rating: item.rating.toFixed(1),
        views: item.views.toFixed()
      }));
    } catch (error) {
      console.error(error);
    }
  },
  computed: {
    sortedData() {
      const { prop, order } = this.sort;
      const data = [...this.tableData];
      if (prop) {
        data.sort((a, b) => {
          if (a[prop] < b[prop]) return order === 'ascending' ? -1 : 1;
          if (a[prop] > b[prop]) return order === 'ascending' ? 1 : -1;
          return 0;

          if (prop === 'views') {
            aValue = Number(aValue);
            bValue = Number(bValue);
          }

          if (aValue < bValue) return order === 'ascending' ? -1 : 1;
          if (aValue > bValue) return order === 'ascending' ? 1 : -1;
        });
      }
      return data;
    },
  },
  methods: {
    handleSort({ prop, order }) {
      this.sort = { prop, order };
    },
  },
}
</script>
<style></style>