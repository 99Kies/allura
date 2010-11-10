import ew

class ProjectSummary(ew.Widget):
    template='jinja:widgets/project_summary.html'
    defaults=dict(
        ew.Widget.defaults,
        value=None)

    def resources(self):
        yield ew.resource.JSLink('js/jquery.tools.min.js')
        yield ew.JSScript('''
        $(document).ready(function() {
            var badges = $('small.badge');
            var i = badges.length;
            while(i){
		        i--;
		    var tipHolder = document.createElement('div');
		    tipHolder.id = "tip"+i;
		    tipHolder.className = "tip";
		    document.body.appendChild(tipHolder)
		    $(badges[i]).parent('a[title]').tooltip({
		        tip: '#tip'+i,
		        opacity: '.9',
		        offset: [-10,0]
		    });
            }
		});
        ''')

class ProjectList(ew.Widget):
    template='jinja:widgets/project_list_widget.html'
    defaults=dict(
        ew.Widget.defaults,
        projects=[],
        project_summary=ProjectSummary(),
        display_mode='list')

    def resources(self):
        for r in self.project_summary.resources():
            yield r
