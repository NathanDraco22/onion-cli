import 'package:flutter_bloc/flutter_bloc.dart';

part 'write_sample_state.dart';

class WriteSampleCubit extends Cubit<WriteSampleState> {
  final SampleEntitiesRepository repository;

  WriteSampleCubit({required this.repository}) : super(WriteSampleInitial());

  Future<void> create(CreateSampleEntity createSampleEntity) async {
    try {
      emit(Writing());
      final item = await repository.createSampleEntity(createSampleEntity);
      emit(ItemCreated(item));
    } catch (e) {
      emit(WriteSampleError(e.toString()));
    }
  }

  Future<void> update(String id, UpdateSampleEntity updateSampleEntity) async {
    try {
      emit(Writing());
      final item = await repository.updateSampleEntityById(id, updateSampleEntity);
      if (item != null) {
        emit(ItemUpdated(item));
      } else {
        emit(WriteSampleError('Item not found'));
      }
    } catch (e) {
      emit(WriteSampleError(e.toString()));
    }
  }

  Future<void> delete(String id) async {
    try {
      emit(Writing());
      final item = await repository.deleteSampleEntityById(id);
      if (item != null) {
        emit(ItemDeleted(item));
      } else {
        emit(WriteSampleError('Item not found'));
      }
    } catch (e) {
      emit(WriteSampleError(e.toString()));
    }
  }
}
