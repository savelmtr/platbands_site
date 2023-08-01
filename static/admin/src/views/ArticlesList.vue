<template>
    <va-card class="markup-tables mb-8">
        <va-card-title>Статьи</va-card-title>
        <table class="va-table va-table--striped va-table--clickable va-table--hoverable">
            <thead>
            <tr>
                <th>Заголовок</th>
                <th>Дата изменения</th>
                <th>Автор</th>
                <th>Статус</th>
            </tr>
            </thead>
            <tbody>
            <tr
                v-for="user in users"
                :key="user.id"
            >
                <td>{{ user.fullName }}</td>
                <td>{{ user.email }}</td>
                <td>{{ user.country }}</td>
                <td>
                <va-badge
                    :text="user.status"
                    :color="user.status"
                />
                </td>
            </tr>
            </tbody>
        </table>
    </va-card>
</template>
<script>
import DefaultLayout from '../layouts/DefaultLayout.vue';

export default {
    name: 'ArticlesList',
    components: {DefaultLayout},
    data() {
    return {
      users: [
        {
          id: 1,
          fullName: "Ashley Mcdaniel",
          email: "ashleymcdaniel@nebulean.com",
          country: "Cayman Islands",
          status: "warning",
        },
        {
          id: 2,
          fullName: "Todd Sellers",
          email: "sellerstodd@nebulean.com",
          country: "Togo",
          status: "info",
        },
        {
          id: 3,
          fullName: "Sherman Knowles",
          email: "shermanknowles@nebulean.com",
          country: "Central African Republic",
          status: "warning",
        },
        {
          id: 4,
          fullName: "Vasquez Lawson",
          email: "vasquezlawson@nebulean.com",
          country: "Bouvet Island",
          status: "info",
        },
      ],
    };
  },
}
</script>
