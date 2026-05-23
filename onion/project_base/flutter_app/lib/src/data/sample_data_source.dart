import 'package:kardex_app_front/src/services/http_service.dart';
import 'package:kardex_app_front/src/tools/http_tool.dart';

class SampleEntitiesDataSource with HttpService {
  SampleEntitiesDataSource._();
  static final SampleEntitiesDataSource instance = SampleEntitiesDataSource._();
  factory SampleEntitiesDataSource() {
    return instance;
  }

  final _endpoint = "/sample_entities";

  Future<Map<String, dynamic>> createSampleEntity(Map<String, dynamic> sampleEntity) async {
    final uri = HttpTools.generateUri(_endpoint);
    final headers = HttpTools.generateAuthHeaders();
    final res = await postQuery(uri, sampleEntity, headers: headers);
    return res;
  }

  Future<Map<String, dynamic>> getAllSampleEntities() async {
    final uri = HttpTools.generateUri(_endpoint);
    final headers = HttpTools.generateAuthHeaders();
    final res = await getQuery(uri, headers: headers);
    return res;
  }

  Future<Map<String, dynamic>?> getSampleEntityById(String sampleEntityId) async {
    final uri = HttpTools.generateUri(_endpoint + "/" + sampleEntityId);
    final headers = HttpTools.generateAuthHeaders();
    final res = await getQuery(uri, headers: headers);
    return res;
  }

  Future<Map<String, dynamic>> searchSampleEntityByKeyword(String keyword) async {
    final uri = HttpTools.generateUri(_endpoint + "/search/" + keyword);
    final headers = HttpTools.generateAuthHeaders();
    final res = await getQuery(uri, headers: headers);
    return res;
  }

  Future<Map<String, dynamic>?> updateSampleEntityById(
    String sampleEntityId,
    Map<String, dynamic> sampleEntity,
  ) async {
    final uri = HttpTools.generateUri(_endpoint + "/" + sampleEntityId);
    final headers = HttpTools.generateAuthHeaders();
    final res = await patchQuery(uri, body: sampleEntity, headers: headers);
    return res;
  }

  Future<Map<String, dynamic>?> deleteSampleEntityById(String sampleEntityId) async {
    final uri = HttpTools.generateUri(_endpoint + "/" + sampleEntityId);
    final headers = HttpTools.generateAuthHeaders();
    final res = await deleteQuery(uri, headers: headers);
    return res;
  }
}