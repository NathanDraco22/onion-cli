import 'package:flutter_bloc/flutter_bloc.dart';

part 'read_sample_state.dart';

class ReadSampleCubit extends Cubit<ReadSampleState> {
  final SampleEntitiesRepository repository;

  ReadSampleCubit({required this.repository}) : super(ReadSampleInitial());

  Future<void> getAll() async {
    try {
      final currentState = state;
      if (currentState is ReadSampleSuccess) {
        emit(ReadSampleRefreshing.fromSuccess(currentState));
      } else {
        emit(ReadSampleLoading());
      }
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

  void markSampleCreated(SampleEntity item) {
    final currentState = state;
    if (currentState is ReadSampleSuccess) {
      final items = [item, ...currentState.items.where((u) => u.id != item.id)];
      final newItems = [...currentState.newItems, item];
      emit(ReadSampleSuccess(items, newItems: newItems));
    }
  }

  void markSampleUpdated(SampleEntity item) {
    final currentState = state;
    if (currentState is ReadSampleSuccess) {
      final items = currentState.items.map((u) => u.id == item.id ? item : u).toList();
      final updatedItems = [...currentState.updatedItems, item];
      emit(ReadSampleSuccess(items, updatedItems: updatedItems));
    }
  }

  void markSampleDeleted(SampleEntity item) {
    final currentState = state;
    if (currentState is ReadSampleSuccess) {
      final deletedItems = [...currentState.deletedItems, item];
      emit(ReadSampleSuccess(currentState.items, deletedItems: deletedItems));
    }
  }
}
