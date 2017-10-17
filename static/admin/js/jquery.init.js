<<<<<<< HEAD
/*global django:true, jQuery:false*/
/* Puts the included jQuery into our own namespace using noConflict and passing
 * it 'true'. This ensures that the included jQuery doesn't pollute the global
 * namespace (i.e. this preserves pre-existing values for both window.$ and
 * window.jQuery).
 */
var django = django || {};
django.jQuery = jQuery.noConflict(true);
=======
/*global django:true, jQuery:false*/
/* Puts the included jQuery into our own namespace using noConflict and passing
 * it 'true'. This ensures that the included jQuery doesn't pollute the global
 * namespace (i.e. this preserves pre-existing values for both window.$ and
 * window.jQuery).
 */
var django = django || {};
django.jQuery = jQuery.noConflict(true);
>>>>>>> 549418614833c8e5b4d8caf88e6746fdc1fb1760
