class SampleEntitiesRepository {
  final SampleEntitiesDataSource sampleEntitiesDataSource;

  SampleEntitiesRepository(this.sampleEntitiesDataSource);

  List<SampleEntity> _sampleEntities = [];

  List<SampleEntity> get sampleEntities => _sampleEntities;

  Future<SampleEntity> createSampleEntity(CreateSampleEntity createSampleEntity) async {
    final result = await sampleEntitiesDataSource.createSampleEntity(createSampleEntity.toJson());
    final newSampleEntity = SampleEntity.fromJson(result);
    _sampleEntities = [newSampleEntity, ..._sampleEntities];
    return newSampleEntity;
  }

  Future<List<SampleEntity>> getAllSampleEntities() async {
    final results = await sampleEntitiesDataSource.getAllSampleEntities();
    final response = ListResponse<SampleEntity>.fromJson(results, SampleEntity.fromJson);

    _sampleEntities = response.data;
    _sampleEntities.sort((a, b) => a.name.toLowerCase().compareTo(b.name.toLowerCase()));
    return _sampleEntities;
  }

  Future<SampleEntity?> getSampleEntityById(String sampleEntityId) async {
    final result = await sampleEntitiesDataSource.getSampleEntityById(sampleEntityId);
    if (result == null) return null;
    return SampleEntity.fromJson(result);
  }

  Future<List<SampleEntity>> searchSampleEntityByKeyword(String keyword) async {
    final result = await sampleEntitiesDataSource.searchSampleEntityByKeyword(keyword);
    final response = ListResponse<SampleEntity>.fromJson(result, SampleEntity.fromJson);
    return response.data;
  }

  Future<List<SampleEntity>> searchSampleEntityByKeywordLocal(String keyword) async {
    final result = sampleEntities.where((u) => u.name.toLowerCase().contains(keyword.toLowerCase())).toList();
    return result;
  }

  Future<SampleEntity?> updateSampleEntityById(String sampleEntityId, UpdateSampleEntity sampleEntity) async {
    final result = await sampleEntitiesDataSource.updateSampleEntityById(sampleEntityId, sampleEntity.toJson());
    if (result == null) return null;

    final updatedSampleEntity = SampleEntity.fromJson(result);
    final index = _sampleEntities.indexWhere((u) => u.id == sampleEntityId);
    if (index != -1) {
      _sampleEntities[index] = updatedSampleEntity;
    }
    return updatedSampleEntity;
  }

  Future<SampleEntity?> deleteSampleEntityById(String sampleEntityId) async {
    final result = await sampleEntitiesDataSource.deleteSampleEntityById(sampleEntityId);
    if (result == null) return null;

    final deletedSampleEntity = SampleEntity.fromJson(result);
    _sampleEntities.removeWhere((u) => u.id == sampleEntityId);
    return deletedSampleEntity;
  }
}
