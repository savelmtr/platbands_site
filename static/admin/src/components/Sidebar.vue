<template>
        <va-sidebar
        >
            <va-sidebar-item
                v-for="item in items"
                :key="item.title"
                :active="item.active"
            >
                <va-sidebar-item-content>
                <va-icon :name="item.icon" />
                    <va-sidebar-item-title>
                        {{ item.title }}
                    </va-sidebar-item-title>
                </va-sidebar-item-content>
            </va-sidebar-item>
        </va-sidebar>
</template>
<script>
export default {
    name: 'Sidebar',
    data() {
        return {
            items: [
                { title: "Посты", icon: "dashboard", active: true },
                { title: "Изображения", icon: "room" },
                { title: "Коллекция наличников", icon: "loop" },
            ]
        }
    },
    created() {
    }
}
</script>