import java.util.Map;

public class Event {

    private Map<String,?> body;

    private Map<String, String> headers;

    private String method;

    private Map<String, String> params;

    private Map<String, String> query;

    public Map<String, ?> getBody() {
        return body;
    }

    public void setBody(Map<String, ?> body) {
        this.body = body;
    }

    public Map<String, String> getHeaders() {
        return headers;
    }

    public void setHeaders(Map<String, String> headers) {
        this.headers = headers;
    }

    public String getMethod() {
        return method;
    }

    public void setMethod(String method) {
        this.method = method;
    }

    public Map<String, String> getParams() {
        return params;
    }

    public void setParams(Map<String, String> params) {
        this.params = params;
    }

    public Map<String, String> getQuery() {
        return query;
    }

    public void setQuery(Map<String, String> query) {
        this.query = query;
    }

    @Override
    public String toString() {
        return "Event{" +
                "body=" + body +
                ", headers=" + headers +
                ", method='" + method + '\'' +
                ", params=" + params +
                ", query=" + query +
                '}';
    }
}
