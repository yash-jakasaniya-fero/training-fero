import { createRouter, createWebHistory } from 'vue-router'
import ContactList from '@/pages/index.vue'
import ContactDetails from '@/pages/ContactDetails.vue'
import AddContact from '@/pages/AddContact.vue'
import ContactUpdate from '@/pages/ContactUpdate.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'contact-list',
      component: ContactList,
    },
    {
      path: '/contact/:id',
      name: 'ContactDetails',
      component: ContactDetails,
    },
    {
      path: '/contact/:id/update',
      name: 'ContactUpdate',
      component: ContactUpdate,
    },
    {
      path: '/add-contact',
      name: 'AddContact',
      component: AddContact
    },
  ],
})

export default router
