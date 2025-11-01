import { createRouter, createWebHistory } from 'vue-router'
import type { RouteLocationNormalized, NavigationGuardNext } from 'vue-router'

const NotFound = () => import("@/components/NotFound.vue")
const WelcomPage = () => import("@/components/WelcomePage.vue")
const CustomerLogin = () => import("@/components/auth/CustomerLogin.vue")
const CustomerRegister = () => import("@/components/auth/CustomerRegister.vue")
const CustomerDashboard = () => import("@/components/CustomerPage/CustomerDashboard.vue")
const Home = () => import("@/components/CustomerPage/home.vue")
const Doors = () => import("@/components/CustomerPage/doors.vue")
const Windows = () => import("@/components/CustomerPage/windows.vue")
const Others = () => import("@/components/CustomerPage/others.vue")
const TrackOrder = () => import("@/components/CustomerPage/TrackOrder.vue")
const ViewUserProfile = ()=> import("@/components/CustomerPage/ViewUserProfile.vue")
const CustomerFeedbackRating = ()=> import("@/components/CustomerPage/FeedbackRating.vue")

const AdminLogin = () => import("@/components/auth/AdminLogin.vue")
const AdminDashboard = () => import("@/components/AdminPage/AdminDashboard.vue")
const MainDashboard = () => import("@/components/AdminPage/MainDashboard.vue")
const RecentActivity = () => import("@/components/AdminPage/RecentActivity.vue")
const ProductManagement = () => import("@/components/AdminPage/ProductManagement.vue")
const OrderManagement = () => import("@/components/AdminPage/OrderManagement.vue")
const AddUpdateProduct = () => import("@/components/AdminPage/AddUpdateProduct.vue")
const AdminFeedbackRating = ()=> import("@/components/AdminPage/ViewFeedback.vue")
const ProductDetail = () => import("@/components/ProductDetail.vue")

const routes = [
    { 
      path: '/admin-login',
      name: 'admin_login', 
      component: AdminLogin,
      beforeEnter: (
        to: RouteLocationNormalized, 
        _from: RouteLocationNormalized, 
        next: NavigationGuardNext
      ) => {
        const secretKey = 'my-secret-key'
        if (to.query.key === secretKey) {
          next() 
        } else {
          next({ path: '/' })
        }
      }
    },

  // Catch all
  { path: '/:pathMatch(.*)*', name: 'not_found', component: NotFound },
  { path: '/', name: 'welcome_page', component: WelcomPage },
  { path: '/login', name: 'login', component: CustomerLogin },
  { path: '/signup', name: 'signup', component: CustomerRegister },
  {
    path: '/dashboard',
    name: 'customer dashboard',
    component: CustomerDashboard,
    redirect: '/dashboard/home',
    children: [
      { path: 'home', name: 'home', component: Home },
      { path: 'doors', name: 'doors', component: Doors },
      { path: 'windows', name: 'windows', component: Windows },
      { path: 'others', name: 'others', component: Others },
      { path: 'track-order', name: 'track order', component: TrackOrder },
      { path: 'user-profile', name: 'user profile', component: ViewUserProfile },
      { path: 'feedback', name: 'feedback rating', component: CustomerFeedbackRating },
      {
        path: '/product/:category/:product_id', name: 'product detail', component: ProductDetail
      },
    ]
  },
  {
    path: '/admin',
    name: 'admin',
    component: AdminDashboard,
    redirect: '/admin/dashboard',
    children: [
      { path: 'dashboard', name: 'dashboard', component: MainDashboard },
      { path: 'recent-activities', name: 'recent activities', component: RecentActivity },
      { path: 'product-management', name: 'product management', component: ProductManagement },
      { path: 'order-management', name: 'order management', component: OrderManagement },
      { path: 'view-feedback', name: 'view feedback', component: AdminFeedbackRating },
    ]

  },
  { path: "/products/add", component: AddUpdateProduct },
  { path: "/products/update/:id", component: AddUpdateProduct, props: true },

]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
