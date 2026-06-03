part of 'read_sample_cubit.dart';

sealed class ReadSampleState {}

final class ReadSampleInitial extends ReadSampleState {}

final class ReadSampleLoading extends ReadSampleState {}

class ReadSampleSuccess extends ReadSampleState {
  final List<SampleEntity> items;
  List<SampleEntity> newItems;
  List<SampleEntity> updatedItems;
  List<SampleEntity> deletedItems;

  ReadSampleSuccess(
    this.items, {
    this.newItems = const [],
    this.updatedItems = const [],
    this.deletedItems = const [],
  });
}

final class ReadSampleRefreshing extends ReadSampleSuccess {
  ReadSampleRefreshing(
    super.items, {
    super.newItems,
    super.updatedItems,
    super.deletedItems,
  });

  factory ReadSampleRefreshing.fromSuccess(
    ReadSampleSuccess success,
  ) =>
      ReadSampleRefreshing(
        success.items,
        newItems: success.newItems,
        updatedItems: success.updatedItems,
        deletedItems: success.deletedItems,
      );
}

final class ReadSampleError extends ReadSampleState {
  final String message;
  ReadSampleError(this.message);
}