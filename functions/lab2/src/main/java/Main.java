import com.amazonaws.services.lambda.runtime.Context;
import com.amazonaws.services.lambda.runtime.RequestHandler;

import java.util.Map;

public class Main implements RequestHandler<Map<String, ?>, String> {

	@Override
	public String handleRequest(Map<String, ?> input, Context context) {
		context.getLogger().log("Start lambda function" + input);
		return "I received an envelope: " + input;
	}
}
