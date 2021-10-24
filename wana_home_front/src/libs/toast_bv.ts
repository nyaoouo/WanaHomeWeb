import { BToast } from 'bootstrap-vue'
class _toast
{
        show(message : string,title : string=''){

          let bootStrapToaster = new BToast();

          bootStrapToaster.$bvToast.toast(message, {
              title: title,
              toaster: "b-toaster-top-center",
              solid: true,
              'auto-hide-delay':1000
            })
        }
}
export const toast= new _toast();
