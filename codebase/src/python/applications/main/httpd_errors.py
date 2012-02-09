TECHNICAL_500_TEMPLATE = """
<div id="summary">
  <h1>{% if exception_type %}{{ exception_type }}{% else %}Report{% endif %}{% if request %} at {{ request.path_info|escape }}{% endif %}</h1>
  <pre class="exception_value">{% if exception_value %}{{ exception_value|force_escape }}{% else %}No exception supplied{% endif %}</pre>
  <table class="meta">
{% if request %}
    <tr>
      <th>Request Method:</th>
      <td>{{ request.META.REQUEST_METHOD }}</td>
    </tr>
    <tr>
      <th>Request URL:</th>
      <td>{{ request.build_absolute_uri|escape }}</td>
    </tr>
{% endif %}
    <tr>
      <th>Django Version:</th>
      <td>{{ django_version_info }}</td>
    </tr>
{% if exception_type %}
    <tr>
      <th>Exception Type:</th>
      <td>{{ exception_type }}</td>
    </tr>
{% endif %}
{% if exception_type and exception_value %}
    <tr>
      <th>Exception Value:</th>
      <td><pre>{{ exception_value|force_escape }}</pre></td>
    </tr>
{% endif %}
{% if lastframe %}
    <tr>
      <th>Exception Location:</th>
      <td>{{ lastframe.filename|escape }} in {{ lastframe.function|escape }}, line {{ lastframe.lineno }}</td>
    </tr>
{% endif %}
    <tr>
      <th>Python Executable:</th>
      <td>{{ sys_executable|escape }}</td>
    </tr>
    <tr>
      <th>Python Version:</th>
      <td>{{ sys_version_info }}</td>
    </tr>
    <tr>
      <th>Python Path:</th>
      <td><pre>{{ sys_path|pprint }}</pre></td>
    </tr>
    <tr>
      <th>Server time:</th>
      <td>{{server_time|date:"r"}}</td>
    </tr>
  </table>
</div>
{% if unicode_hint %}
<div id="unicode-hint">
    <h2>Unicode error hint</h2>
    <p>The string that could not be encoded/decoded was: <strong>{{ unicode_hint|force_escape }}</strong></p>
</div>
{% endif %}
{% if template_does_not_exist %}
    <div id="template-not-exist">
        <h2>Template-loader postmortem</h2>
        {% if loader_debug_info %}
            <p>Django tried loading these templates, in this order:</p>
            <ul>
            {% for loader in loader_debug_info %}
                <li>Using loader <code>{{ loader.loader }}</code>:
                    <ul>{% for t in loader.templates %}<li><code>{{ t.name }}</code> (File {% if t.exists %}exists{% else %}does not exist{% endif %})</li>{% endfor %}</ul>
                </li>
            {% endfor %}
            </ul>
        {% else %}
            <p>Django couldn't find any templates because your <code>TEMPLATE_LOADERS</code> setting is empty!</p>
        {% endif %}
    </div>
{% endif %}
{% if template_info %}
    <div id="template">
       <h2>Template error</h2>
       <p>In template <code>{{ template_info.name }}</code>, error at line <strong>{{ template_info.line }}</strong></p>
       <h3>{{ template_info.message }}</h3>
       <table class="source{% if template_info.top %} cut-top{% endif %}{% ifnotequal template_info.bottom template_info.total %} cut-bottom{% endifnotequal %}">
       {% for source_line in template_info.source_lines %}
           {% ifequal source_line.0 template_info.line %}
               <tr class="error"><th>{{ source_line.0 }}</th>
               <td>{{ template_info.before }}<span class="specific">{{ template_info.during }}</span>{{ template_info.after }}</td></tr>
           {% else %}
              <tr><th>{{ source_line.0 }}</th>
              <td>{{ source_line.1 }}</td></tr>
           {% endifequal %}
       {% endfor %}
       </table>
    </div>
{% endif %}
{% if frames %}
    <div id="traceback">
      <h2>Traceback</h2>
      {% autoescape off %}
          <div id="browserTraceback">
            <ul class="traceback">
              {% for frame in frames %}
                <li class="frame">
                  <code>{{ frame.filename|escape }}</code> in <code>{{ frame.function|escape }}</code>
                  {% if frame.context_line %}
                      <ul><li><pre>{{ frame.lineno }}: {{ frame.context_line|escape }}</pre></li></ol>
                  {% endif %}
                </li>
              {% endfor %}
            </ul>
          </div>
      {% endautoescape %}
    </div>
{% endif %}

<div id="requestinfo">
  <h2>Request information</h2>

{% if request %}
  <h3 id="get-info">GET</h3>
  {% if request.GET %}
    <table class="req">
      <thead>
        <tr>
          <th>Variable</th>
          <th>Value</th>
        </tr>
      </thead>
      <tbody>
        {% for var in request.GET.items %}
          <tr>
            <td>{{ var.0 }}</td>
            <td class="code"><pre>{{ var.1|pprint }}</pre></td>
          </tr>
        {% endfor %}
      </tbody>
    </table>
  {% else %}
    <p>No GET data</p>
  {% endif %}

  <h3 id="post-info">POST</h3>
  {% if request.POST %}
    <table class="req">
      <thead>
        <tr>
          <th>Variable</th>
          <th>Value</th>
        </tr>
      </thead>
      <tbody>
        {% for var in request.POST.items %}
          <tr>
            <td>{{ var.0 }}</td>
            <td class="code"><pre>{{ var.1|pprint }}</pre></td>
          </tr>
        {% endfor %}
      </tbody>
    </table>
  {% else %}
    <p>No POST data</p>
  {% endif %}
  <h3 id="files-info">FILES</h3>
  {% if request.FILES %}
    <table class="req">
        <thead>
            <tr>
                <th>Variable</th>
                <th>Value</th>
            </tr>
        </thead>
        <tbody>
            {% for var in request.FILES.items %}
                <tr>
                    <td>{{ var.0 }}</td>
                    <td class="code"><pre>{{ var.1|pprint }}</pre></td>
                </tr>
            {% endfor %}
        </tbody>
    </table>
  {% else %}
    <p>No FILES data</p>
  {% endif %}


  <h3 id="cookie-info">COOKIES</h3>
  {% if request.COOKIES %}
    <table class="req">
      <thead>
        <tr>
          <th>Variable</th>
          <th>Value</th>
        </tr>
      </thead>
      <tbody>
        {% for var in request.COOKIES.items %}
          <tr>
            <td>{{ var.0 }}</td>
            <td class="code"><pre>{{ var.1|pprint }}</pre></td>
          </tr>
        {% endfor %}
      </tbody>
    </table>
  {% else %}
    <p>No cookie data</p>
  {% endif %}

  <h3 id="meta-info">META</h3>
  <table class="req">
    <thead>
      <tr>
        <th>Variable</th>
        <th>Value</th>
      </tr>
    </thead>
    <tbody>
      {% for var in request.META.items|dictsort:"0" %}
        <tr>
          <td>{{ var.0 }}</td>
          <td class="code"><pre>{{ var.1|pprint }}</pre></td>
        </tr>
      {% endfor %}
    </tbody>
  </table>
{% else %}
  <p>Request data not supplied</p>
{% endif %}

  <h3 id="settings-info">Settings</h3>
  <h4>Using settings module <code>{{ settings.SETTINGS_MODULE }}</code></h4>
  <table class="req">
    <thead>
      <tr>
        <th>Setting</th>
        <th>Value</th>
      </tr>
    </thead>
    <tbody>
      {% for var in settings.items|dictsort:"0" %}
        <tr>
          <td>{{ var.0 }}</td>
          <td class="code"><pre>{{ var.1|pprint }}</pre></td>
        </tr>
      {% endfor %}
    </tbody>
  </table>

</div>
"""

FLAT_500_TEMPLATE = """
SERVER ERROR CODE: 500
Server time      : {{server_time|date:"r"}}
====================================================================================================
{% if exception_type %}{{ exception_type }}{% else %}Report{% endif %}{% if request %} at {{ request.path_info|escape }}{% endif %}
{% if exception_value %}{{ exception_value|force_escape }}{% else %}No exception supplied{% endif %}
====================================================================================================
Django Version    : {{ django_version_info }}
Python Version    : {{ sys_version_info }}
Python Executable : {{ sys_executable|escape }}
Python Path       : {% autoescape off %}{{ sys_path }}{% endautoescape %}
----------------------------------------------------------------------------------------------------
{% if request %}Request Method     : {{ request.META.REQUEST_METHOD }}\nRequest URL        : {{ request.build_absolute_uri|escape }}{% endif %}
{% if exception_type %}Exception Type     : {{ exception_type }}{% if exception_value %}\nException Value    : {{ exception_value|force_escape }}{% endif %}{% endif %}
{% if lastframe %}Exception Location : {{ lastframe.filename|escape }} in {{ lastframe.function|escape }}, line {{ lastframe.lineno }}{% endif %}
----------------------------------------------------------------------------------------------------
{% if unicode_hint %}Unicode error hint : The string that could not be encoded/decoded was: {{ unicode_hint|force_escape }}{% endif %}
{% if template_does_not_exist %}Template-loader postmortem:{% if loader_debug_info %}Django tried loading these templates, in this order:{% for loader in loader_debug_info %}    Using loader {{ loader.loader }}:{% for t in loader.templates %}        {{ t.name }} (File {% if t.exists %}exists{% else %}does not exist{% endif %}){% endfor %}{% endfor %}{% else %}Django couldn't find any templates because your TEMPLATE_LOADERS setting is empty!{% endif %}{% endif %}
{% if template_info %}Template error:In template {{ template_info.name }}, error at line {{ template_info.line }}{{ template_info.message }}{% for source_line in template_info.source_lines %}{% ifequal source_line.0 template_info.line %}{{ source_line.0 }}: {{ template_info.before }}{{ template_info.during }}{{ template_info.after }}\n{% else %}{{ source_line.0 }}: {{ source_line.1 }}\n{% endifequal %}{% endfor %}{% endif %}
----------------------------------------------------------------------------------------------------
{% if frames %}\nStack Trace:\n{% autoescape off %}{% for frame in frames %}   {{ frame.filename }} in {{ frame.function }}{% if frame.context_line %}\n      #{{ frame.pre_context_lineno }}. {{ frame.context_line }}\n{% endif %}{% endfor %}{% endautoescape %}{% else %}No stack trace available.{% endif %}
----------------------------------------------------------------------------------------------------
{% if request.GET %}GET Data: {% for var in request.GET.items %}\n   '{{ var.0 }}' = '{{ var.1 }}'{% endfor %}{% else %}No GET data{% endif %}
{% if request.POST %}POST Data: {% for var in request.POST.items %}\n   '{{ var.0 }}' = '{{ var.1 }}'{% endfor %}{% else %}No POST data{% endif %}
{% if request.FILES %}FILES Data: {% for var in request.FILES.items %}\n   '{{ var.0 }}' = '{{ var.1 }}'{% endfor %}{% else %}No FILES{% endif %}
{% if request.COOKIES %}COOKIES Data: {% for var in request.COOKIES.items %}\n   '{{ var.0 }}' = '{{ var.1 }}'{% endfor %}{% else %}No COOKIES{% endif %}
{% if request.META %}META Data: {% for var in request.META.items %}\n   '{{ var.0 }}' = '{{ var.1 }}'{% endfor %}{% else %}No META{% endif %}
"""

TECHNICAL_404_TEMPLATE = """
  <div id="summary">
    <h1>Page not found <span>(404)</span></h1>
    <table class="meta">
      <tr>
        <th>Request Method:</th>
        <td>{{ request.META.REQUEST_METHOD }}</td>
      </tr>
      <tr>
        <th>Request URL:</th>
      <td>{{ request.build_absolute_uri|escape }}</td>
      </tr>
    </table>
  </div>
  <div id="info">
    {% if urlpatterns %}
      <p>
      Using the URLconf defined in <code>{{ urlconf }}</code>,
      Django tried these URL patterns, in this order:
      </p>
      <ol>
        {% for pattern in urlpatterns %}
          <li>
            {% for pat in pattern %}
                {{ pat.regex.pattern }}
                {% if forloop.last and pat.name %}[name='{{ pat.name }}']{% endif %}
            {% endfor %}
          </li>
        {% endfor %}
      </ol>
      <p>The current URL, <code>{{ request_path|escape }}</code>, didn't match any of these.</p>
    {% else %}
      <p>{{ reason }}</p>
    {% endif %}
  </div>
"""

FLAT_404_TEMPLATE = """
SERVER ERROR CODE: 404 PAGE NOT FOUND
====================================================================================================
Request Method : {{ request.META.REQUEST_METHOD }}
Request URL    : {{ request.build_absolute_uri }}
====================================================================================================
{% if urlpatterns %}Using the URLconf defined in {{ urlconf }}, Django tried these URL patterns, in this order:\n{% for pattern in urlpatterns %}{% for pat in pattern %}   {{ pat.regex.pattern }}\n{% if forloop.last and pat.name %}[name='{{ pat.name }}']{% endif %}{% endfor %}{% endfor %}The current URL, {{ request_path }}, didn't match any of these.{% else %}{{ reason }}{% endif %}
"""
