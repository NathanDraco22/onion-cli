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

final class ReadSampleSearching extends ReadSampleSuccess {
  ReadSampleSearching(
    super.items, {
    super.newItems,
    super.updatedItems,
    super.deletedItems,
  });
}

class HighlightedSampleItem extends ReadSampleSuccess {
  HighlightedSampleItem(
    super.items, {
    super.newItems,
    super.updatedItems,
    super.deletedItems,
  });
}

final class ReadSampleError extends ReadSampleState {
  final String message;
  ReadSampleError(this.message);
}