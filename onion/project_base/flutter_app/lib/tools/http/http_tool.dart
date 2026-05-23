import 'package:http/http.dart' as http;

class HttpTools {
  static const String _baseUrl = 'http://localhost:8000';

  static Uri generateUri(String path, {Map<String, dynamic>? queryParams}) {
    final uri = Uri.parse('$_baseUrl$path');
    if (queryParams != null && queryParams.isNotEmpty) {
      return uri.replace(queryParameters: queryParams.map(
        (key, value) => MapEntry(key, value.toString()),
      ));
    }
    return uri;
  }

  static Map<String, String> generateAuthHeaders({Map<String, String>? additional}) {
    final headers = <String, String>{
      'Content-Type': 'application/json',
      'Accept': 'application/json',
    };
    if (additional != null) {
      headers.addAll(additional);
    }
    return headers;
  }
}