import 'package:flutter_bloc/flutter_bloc.dart';

part 'read_sample_state.dart';

class ReadSampleCubit extends Cubit<ReadSampleState> {
  final SampleEntitiesRepository repository;

  ReadSampleCubit({required this.repository}) : super(ReadSampleInitial());

  Future<void> getAll() async {
    try {
      emit(ReadSampleLoading());
      final items = await repository.getAllSampleEntities();
      emit(ReadSampleSuccess(items));
    } catch (e) {
      emit(ReadSampleError(e.toString()));
    }
  }

  Future<void> getById(String id) async {
    try {
      emit(ReadSampleLoading());
      final item = await repository.getSampleEntityById(id);
      if (item != null) {
        emit(ReadSampleSuccess([item]));
      } else {
        emit(ReadSampleError('Item not found'));
      }
    } catch (e) {
      emit(ReadSampleError(e.toString()));
    }
  }

  void markSampleUpdated(SampleEntity item) {
    final currentState = state;
    if (currentState is ReadSampleSuccess) {
      final updatedItems = [...currentState.updatedItems, item];
      emit(ReadSampleSuccess(currentState.items, updatedItems: updatedItems));
    }
  }

  void putSampleFirst(SampleEntity item) {
    final currentState = state;
    if (currentState is ReadSampleSuccess) {
      final items = [item, ...currentState.items.where((u) => u.id != item.id)];
      emit(ReadSampleSuccess(items, updatedItems: [item]));
    }
  }
}
