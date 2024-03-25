document.addEventListener('DOMContentLoaded', function() {
  var WcdSideBarApplicationPinning = function(sidebarSelector) {
      this.sidebar = document.querySelector(sidebarSelector);
  };

  WcdSideBarApplicationPinning.prototype = {
      pinToggle: function(form, appItem) {
          var self = this;
          var appsList = this.sidebar.querySelector('.apps-list');
          var pinnedAppsList = this.sidebar.querySelector('.apps-list-pinned');
          var formData = new FormData(form);
          fetch(form.action, {
              method: form.method,
              body: formData
            })
            .then(response => response.json())
            .then(result => {
              if (result.error) {
                  return;
                }
                
                window.location.reload();
                var target = result.pinned ? pinnedAppsList : appsList;
                appItem.classList.toggle('pinned', result.pinned);
                
            //   target.appendChild(appItem);
            //   self.updateAppsHide();
          })
          .catch(error => console.error('Error:', error));
      },
      initApplicationPinning: function() {
          var self = this;
          var pinToggles = this.sidebar.querySelectorAll('.wcd-pin-toggle');
          pinToggles.forEach(function(toggle) {
              toggle.addEventListener('click', function(e) {
                 
                  e.preventDefault();
                  e.stopPropagation();

                  var appItem = this.closest('.app-item');
                  var appLabel = appItem.getAttribute('data-app-label');
                  var form = self.sidebar.querySelector('#toggle-application-pin-form');

                  form.querySelector('input[name="app_label"]').value = appLabel;

                  self.pinToggle(form, appItem);
              });
          });

          this.sidebar.querySelector('.edit-apps-list').addEventListener('click', function(e) {
              e.preventDefault();
              this.closest('.sidebar-section').classList.toggle('editing');
          });
      },
      updateAppsHide: function() {
          var appsList = this.sidebar.querySelector('.apps-list');
          var pinnedAppsList = this.sidebar.querySelector('.apps-list-pinned');
          var appsHide = this.sidebar.querySelector('.apps-hide');

          if ((appsList.children.length === 0 || pinnedAppsList.children.length === 0) && appsList.style.display !== 'none') {
              appsHide.classList.remove('apps-visible', 'apps-hidden');
          } else {
              appsHide.classList.toggle('apps-visible', appsList.style.display !== 'none');
              appsHide.classList.toggle('apps-hidden', appsList.style.display === 'none');
          }
      },
      initAppsHide: function() {
        //   var self = this;
        //   var appsList = this.sidebar.querySelector('.apps-list');
        //   var pinnedAppsList = this.sidebar.querySelector('.apps-list-pinned');
        //   var appsHide = this.sidebar.querySelector('.apps-hide');

        //   appsHide.addEventListener('click', function(e) {
        //       e.preventDefault();

        //       var isVisible = appsList.style.display !== 'none';
        //       appsList.style.display = isVisible ? 'none' : 'block';
        //       localStorage.setItem('side_menu_apps_list_visible', !isVisible);
        //       self.updateAppsHide();
        //   });

        //   if (localStorage.getItem('side_menu_apps_list_visible') === 'false') {
        //       if (pinnedAppsList.children.length !== 0) {
        //           appsList.style.display = 'none';
        //       } else {
        //           localStorage.setItem('side_menu_apps_list_visible', 'true');
        //       }
        //   }

        //   this.updateAppsHide();
      },
      run: function() {
          try {
              this.initApplicationPinning();
            //   this.initAppsHide();
          } catch (e) {
              console.error(e, e.stack);
          }
      }
  };

  var sidebarApp = new WcdSideBarApplicationPinning('.sidebar');
  sidebarApp.run();
});
